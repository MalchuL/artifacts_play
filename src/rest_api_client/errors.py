class ArtifactsHTTPStatusError(Exception):
    """Raised by api functions when the response status an undocumented status and
    Client.raise_on_unexpected_status is True."""

    def __init__(self, status_code: int, content: bytes, json: dict):
        self.status_code = status_code
        self.content = content
        self.json = json

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )
