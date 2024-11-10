from src.rest_api_client.api.named_classes import ObjectCodeRequest, PagedRequest
from src.rest_api_client.model import DataPageTaskFullSchema, TaskFullResponseSchema, \
    DataPageDropRateSchema, TasksRewardResponseSchema


class GetAllTasks(PagedRequest):
    """
    Get All Tasks
    Fetch the list of all tasks.
    operationId: get_all_tasks_tasks_list_get
    """
    endpoint_pattern = '/tasks/list'
    method_name = 'get'
    response_schema = DataPageTaskFullSchema
    error_responses = {}

    def __call__(self) -> DataPageTaskFullSchema:
        return super().__call__(None)


class GetTask(ObjectCodeRequest):
    """
    Get Task
    Retrieve the details of a task.
    operationId: get_task_tasks_list__code__get
    """
    endpoint_pattern = '/tasks/list/{code}'
    method_name = 'get'
    response_schema = TaskFullResponseSchema
    error_responses = {404: 'Task not found.'}

    def __call__(self) -> TaskFullResponseSchema:
        return super().__call__(None)


class GetAllTasksRewards(PagedRequest):
    """
    Get All Tasks Rewards
    Fetch the list of all tasks rewards. To obtain these rewards, you must exchange 6 task coins with a tasks master.
    operationId: get_all_tasks_rewards_tasks_rewards_get
    """
    endpoint_pattern = '/tasks/rewards'
    method_name = 'get'
    response_schema = DataPageDropRateSchema
    error_responses = {}

    def __call__(self) -> DataPageDropRateSchema:
        return super().__call__(None)


class GetTasksReward(ObjectCodeRequest):
    """
    Get Tasks Reward
    Retrieve the details of a tasks reward.
    operationId: get_tasks_reward_tasks_rewards__code__get
    """
    endpoint_pattern = '/tasks/rewards/{code}'
    method_name = 'get'
    response_schema = TasksRewardResponseSchema
    error_responses = {404: 'Tasks reward not found.'}

    def __call__(self) -> TasksRewardResponseSchema:
        return super().__call__(None)
