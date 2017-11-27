"""A mapping of file extensions to MIME type strings."""

MIME_MAP = {
    # application
    '.arc': 'application/octet-stream',
    '.bin': 'application/octet-stream',
    '.bz': 'application/x-bzip',
    '.bz2': 'application/x-bzip2',
    '.gzip': 'application/gzip',
    '.gz': 'application/gzip',
    '.json': 'application/json',
    '.pdf': 'application/pdf',
    '.rar': 'application/x-rar-compressed',
    # application/vnd.rar
    '.tar': 'application/x-tar',
    '.xhtml': 'application/xhtml+xml',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.ms-excel',
    '.zip': 'application/zip',
    '.zlib': 'application/zlib',
    # text
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.rtf': 'text/rtf',
    '.xml': 'text/xml',
}
