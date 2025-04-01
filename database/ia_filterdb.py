import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, MAX_BTN

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(DATABASE_URI)
mydb = client[DATABASE_NAME]
instance = Instance.from_db(mydb)

# Collection for filter words
filter_words_collection = mydb["filter_words"]

# Default filter words
DEFAULT_FILTER_WORDS = {
    'bhai', 'bhje do', 'send', 'please', 'hai', 'hai kya', 'kya', 
    'do', 'de do', 'chahiye', 'dijiye', 'dedo', 'south',
    'gurnal', 'bhular', 'movie', 'series', 'anime', 'link',
    'download', 'de', 'dear', 'bro', 'hi', 'hello', 'pls', 'plz'
}

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)
    file_type = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

async def get_filter_words():
    """Get current filter words from database"""
    try:
        doc = await filter_words_collection.find_one({"_id": "filter_words"})
        if doc:
            return set(doc["words"])
        # Initialize with default words if not exists
        await set_filter_words(DEFAULT_FILTER_WORDS)
        return DEFAULT_FILTER_WORDS
    except Exception as e:
        logger.error(f"Error getting filter words: {e}")
        return DEFAULT_FILTER_WORDS

async def set_filter_words(words):
    """Update filter words in database"""
    try:
        words_list = list(words) if isinstance(words, set) else words
        await filter_words_collection.update_one(
            {"_id": "filter_words"},
            {"$set": {"words": words_list}},
            upsert=True
        )
        logger.info("Filter words updated successfully")
    except Exception as e:
        logger.error(f"Error setting filter words: {e}")

async def get_files_db_size():
    return (await mydb.command("dbstats"))['dataSize']

async def save_file(media):
    """Save file in database"""
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    caption = media.caption.html if media.caption else media.file_name

    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            mime_type=media.mime_type,
            caption=caption,
            file_type=media.mime_type.split('/')[0]
        )
    except ValidationError:
        logger.error('Error occurred while saving file in database')
        return 'err'
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is already saved in database')
            return 'dup'
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to database')
            return 'suc'

async def get_search_results(query, max_results=MAX_BTN, offset=0, lang=None):
    """Improved search that handles queries with extra text"""
    query = query.strip()
    
    # Get current filter words
    filter_words = await get_filter_words()
    
    if not query:
        raw_pattern = '.'
    else:
        search_terms = extract_search_terms(query, filter_words)
        raw_pattern = build_regex_pattern(search_terms)
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except re.error as e:
        logger.error(f"Regex error for pattern '{raw_pattern}': {e}")
        regex = query

    # Search in both file_name and caption
    filter = {
        '$or': [
            {'file_name': regex},
            {'caption': regex}
        ]
    }

    cursor = Media.find(filter)
    cursor.sort('$natural', -1)

    if lang:
        lang_files = [file async for file in cursor if lang in (file.file_name or '').lower() or lang in (file.caption or '').lower()]
        files = lang_files[offset:][:max_results]
        total_results = len(lang_files)
        next_offset = offset + max_results
        if next_offset >= total_results:
            next_offset = ''
        return files, next_offset, total_results

    cursor.skip(offset).limit(max_results)
    files = await cursor.to_list(length=max_results)
    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results
    if next_offset >= total_results:
        next_offset = ''       
    return files, next_offset, total_results

async def get_bad_files(query, file_type=None, offset=0, filter=False):
    query = query.strip()
    if not query:
        raw_pattern = '.'
    else:
        search_terms = extract_search_terms(query)
        raw_pattern = build_regex_pattern(search_terms)
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except re.error:
        return [], 0

    filter = {
        '$or': [
            {'file_name': regex},
            {'caption': regex}
        ]
    }

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    cursor = Media.find(filter)
    cursor.sort('$natural', -1)
    files = await cursor.to_list(length=total_results)
    return files, total_results

async def get_file_details(query):
    filter = {
        '$or': [
            {'file_id': query},
            {'file_name': query},
            {'caption': query}
        ]
    }
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")

def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")

def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref
