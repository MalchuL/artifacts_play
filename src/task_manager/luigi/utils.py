def log_job(logger, job_text):
    string = "-" * 10
    string += f" {job_text} "
    string += "-" * 10
    logger.info(string)
