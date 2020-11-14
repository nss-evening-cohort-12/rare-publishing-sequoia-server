class Comment():
    def __init__(self, id, subject, content, post_id, user_id, publication_date):
        self.id = id
        self.subject = subject
        self.content = content
        self.post_id = post_id
        self.user_id = user_id
        self.publication_date = publication_date
        self.user = None
