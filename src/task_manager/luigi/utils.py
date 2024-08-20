from logging import Logger


def log_job(job_text: str, logger: Logger):
    string = "-" * 10
    string += f" {job_text} "
    string += "-" * 10
    logger.info(string)
