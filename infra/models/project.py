class AmericaProject:
    def __init__(self,
                 url: str,
                 files: list = None,
                 type: str = None,
                 user: str = None,
                 users: list = None,
                 jira_id: id = None,
                 type_key: str = None,
                 description: str = None,
                 category_id: int = None,
                 america_uuid: str = None,
                 assignee_type: str = None,
                 project_template_key: str = None,
                 workflow_scheme_id: int = None):
         self.key = key
         self.name = name
         self.user = user
         self.users = users
         self.jira_id = jira_id
         self.type_key = type_key
         self.description = description
         self.category_id = category_id
         self.assignee_type = assignee_type
         self.project_template_key = project_template_key
         self.workflow_scheme_id = workflow_scheme_id

    def to_jira(self) -> dict:
        object_dict = {
            'key': self.key,
            'name': self.name,
            'lead': self.user,
            'projectTypeKey': self.type_key,
            'description': self.description,
            'categoryId': self.category_id,
            'assigneeType': self.assignee_type,
            'projectTemplateKey': self.project_template_key,
            'workflowSchemeId': self.workflow_scheme_id
        }

        # remove `None` values from the dict
        object_dict = {k: v for k, v in object_dict.items() if v is not None}

        return object_dict

    def to_america(self) -> dict:
        object_dict = {
            'id': self.america_uuid,
            'name': self.name,
            'type': self.type,
            'user': self.user,
            'users': self.users,
            'properties': {
                'name': self.name,
                'id': self.jira_id,
                'key': self.key,
                'description': self.description,
                'projectCategory': self.category_id,
                'assigneeType': self.assignee_type,
                'projectTypeKey': self.type_key,
                'projectTemplateKey': self.project_template_key
            }
        }

        # remove `None` values from the dict
        object_dict = {k: v for k, v in object_dict.items() if v is not None}

        return object_dict

    @staticmethod
    def from_america(data: dict) -> 'AmericaProject':
        if data.get('properties') is None:
            data.__setitem__('properties', {})

        return AmericaProject(america_uuid=data.get('id'),
                              name=data.get('properties').get('name'),
                              type=data.get('template_name'),
                              user=data.get('properties').get('user'),
                              users=data.get('properties').get('users'),
                              key=data.get('properties').get('key'),
                              jira_id=data.get('properties').get('id'),
                              type_key=data.get('properties').get('projectTypeKey'),
                              description=data.get('properties').get('description'),
                              category_id=data.get('properties').get('projectCategory'),
                              assignee_type=data.get('properties').get('assigneeType'),
                              project_template_key=data.get('properties').get('projectTemplateKey'))

    @staticmethod
    def from_jira(data: dict) -> 'AmericaProject':
        lead = data.get('lead')
        if type(lead) == dict:
            lead = lead['key']

        if type(data.get('projectCategory')) == dict:
            category_id = data.get('projectCategory')['id']
        else:
            category_id = None

        return AmericaProject(user=lead,
                              jira_id=data.get('id'),
                              key=data.get('key'),
                              name=data.get('name'),
                              category_id=category_id,
                              description=data.get('description'),
                              type_key=data.get('projectTypeKey'),
                              assignee_type=data.get('assigneeType'),
                              project_template_key=data.get('projectTemplateKey'))

    def __eq__(self, other: 'AmericaProject') -> bool:
        return self.key == other.key \
               and self.name == other.name \
               and int(self.jira_id) == int(other.jira_id) \
               and self.type_key == other.type_key \
               and self.description == other.description \
               and int(self.category_id) == int(other.category_id) \
               and self.assignee_type == other.assignee_type
