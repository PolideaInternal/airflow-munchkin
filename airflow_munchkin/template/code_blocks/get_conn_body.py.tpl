if not self._client:
    self._client = {{ client.name }}(credentials=self._get_credentials())
return self._client
