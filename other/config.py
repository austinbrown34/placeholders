import os


BMP_FILE_PATTERN = '.%dx%d.bmp'
IMG_FILE_PATTERN = '.%d.%dx%d.img'
TEMPLATE_INTERNAL_ID_KEYWORD = 'internal_id'
TEMPLATE_CONFIG_FILE = 'config.yaml'
TEMPLATE_SCRIPTS_KEYWORD = 'template_scripts'
TEMPLATE_INCLUDED_TEMPLATES_KEYWORD = 'included_templates'
TEMPLATE_RULE_KEYWORD = 'rule'
TEMPLATE_PACKAGE_KEY_KEYWORD = 'package_key'
TEMPLATE_PACKAGE_NAME_KEYWORD = 'package_name'
TEMPLATE_LOGO_KEYWORD = 'template_logo'
TEMPLATE_USER_KEYWORD = 'user'
NO_TEMPLATE_USER_KEYWORD = ' ? '
TEMPLATE_RULES_KEYWORD = 'template_rules'
SAMPLE_JPG = 'sample.jpg'
TEMP_PLACEHOLDERS_FOLDER_NAME = 'placeholders'
SPARKLINE_HTML_SUFFIX = '-sparkline.html'
SPARKLINE_SUFFIX = '_with_sparkline'
SPLIT_SUFFIX = '_split'
FONT_SUFFIX = '_fontsize'
VIZ_PREFIX = 'viz_'
FORM_FILL_TOKEN = '::'
PLACEHOLDER_TOKEN = '.'
TEMP_PDF_PATTERN = 'temp{}.pdf'
TEMP_IMAGE_PDF_PATTERN = 'tempimage{}.pdf'
DRAW_IMAGES_TEMP_SUFFIX = '_temp'
REPAIR_SUFFIX = '_fixed.pdf'
JPG_FILE_PATTERN = '{}jpg%d.jpg'
PLACEHOLDER_TEMP_SUFFIX = '_temp.pdf'
JPG_END_MARK = "\xff\xd9"
JPG_START_MARK = "\xff\xd8"
DUMP_DATA_FIELDS_FILE = 'dump_data_fields.txt'
DEFAULT_PDF_PASSWORD = 'longlivethegreen'
MAKE_FDF_FILE = 'make_fdf.js'
FDF_FOLDER_NAME = 'fdf'
FDF_FOLDER_PATH = '/tmp/fdf'
WORK_COMPLETE_PATTERN = 'work_complete{}.pdf'
WORK_COMPLETE_TEMP_PATTERN = 'work_complete_temp{}.pdf'
FILLED_IMAGES_PATTERN = 'work_filled_with_images{}.pdf'
FILLED_NO_PLACEHOLDERS_PATTERN = 'work_filled_noplaceholders{}.pdf'
FILLED_FILE_PATTERN = 'work_filled{}.pdf'
FDF_FILE_PATTERN = 'work{}.fdf'
XML_FILE_PATTERN = 'work{}.xml'
TEMP_FOLDER_NAME = 'temp'
BASE_FOLDER = '/tmp'
MERGED_REPORT_NAME = 'Final_PDF.pdf'
REPAIRED_REPORT_NAME = 'Final_PDF_fixed_unsafe.pdf'
FINAL_REPORT_NAME = 'Final_PDF_fixed.pdf'
SAVED_REPORT_NAME = 'finalpdf.pdf'
WORK_FOLDER = '/tmp/work'
WORK_FOLDER_NAME = 'work'
LOCAL_KEYWORD = 'run_local'
BINARIES_FOLDER = '/bin'
FONTCONFIG_BASE = 'fontconfig'
FONTCONFIG_LIB_PATH = '/fontconfig/usr/lib'
PDF_LINK_BUCKET = 'pdf-links'
PDF_LINK_NAME = 'finalpdf.pdf'
JOB_TYPE_KEYWORD = 'job_type'
JOB_TYPES_FOLDER = 'job_types'
DELIVERY_METHOD_KEYWORD = 'delivery_method'
CALLBACK_KEYWORD = 'post_data'
SERVER_DATA_KEYWORD = 'pdf_data'
REDIRECT_URL_KEYWORD = 'redirect_url'
REDIRECT_URL_BASE_KEYWORD = 'redirect_url_base'
RECEIVED_API_KEY_KEYWORD = 'api_key'
RECEIVED_API_SECRET_KEYWORD = 'api_secret'
POST_FILE_KEYWORD = 'POST_FILE'
POST_LINK_KEYWORD = 'POST_LINK'
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '')
CURR_BIN_DIR = 'bin'
BIN_DIR = '/tmp/bin'
LAMBDA_PATH = '{}:{}{}'.format(
    os.environ.get('PATH', ''),
    os.environ.get('LAMBDA_TASK_ROOT', ''),
    BINARIES_FOLDER
)
LAMBDA_LD_LIBRARY_PATH = '{}{}'.format(
    os.environ.get('LAMBDA_TASK_ROOT', ''),
    BINARIES_FOLDER
)
FC_CACHE_PATH = '/tmp/fontconfig/usr/bin/fc-cache'
POSTED_API_KEY_KEYWORD = 'API_KEY'
POSTED_API_SECRET_KEYWORD = 'API_SECRET'
VIZ_FOLDER_NAME = 'viz'
VIZ_JS_FOLDER_NAME = 'js'
VIZ_JS_CONTROLLER = 'controller.js'
VIZ_HTML_FOLDER_NAME = 'html'
PIECHART_FOLDER_NAME = 'piechart'
PIECHART_COLORS_FILE = 'colors.js'
PHANTOMJS_CONTROL_FILE = 'report.js'
PDFTK = os.path.join(BASE_FOLDER, CURR_BIN_DIR, 'pdftk')
LD_LIBRARY_PATH = os.path.join(BASE_FOLDER, CURR_BIN_DIR)
LIBGCJ = os.path.join(BASE_FOLDER, CURR_BIN_DIR, 'libgcj.so.10')
PHANTOMJS = os.path.join(BASE_FOLDER, CURR_BIN_DIR, 'phantomjs')
