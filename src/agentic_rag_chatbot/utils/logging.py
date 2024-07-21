import logging

from agentic_rag_chatbot.utils.config import get_params


params = get_params()
module_name = params['module_name']

logger = logging.getLogger(module_name)

logger.setLevel(logging.INFO)

logging_format = '\n%(asctime)s | %(name)s | %(levelname)s | %(message)s'
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(logging.Formatter(logging_format))
logger.addHandler(c_handler)
