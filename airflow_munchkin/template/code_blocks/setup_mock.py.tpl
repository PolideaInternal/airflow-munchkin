with mock.patch(
    '{{ class_path }}.__init__',
    new={{ new }},
):
    self.hook = {{ class_path | to_class_name }}(gcp_conn_id='test')
