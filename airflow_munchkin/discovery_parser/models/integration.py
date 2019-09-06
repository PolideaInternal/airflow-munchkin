# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Optional


class DiscoveryIntegration(NamedTuple):
    api_path: str
    version: str
    service_name: str
    object_name: str
    package_name: str
    file_prefix: str = ""
    class_prefix: str = ""
    methods: Optional[List[str]] = None
    """
    :param api_path: discovery api path, in form of:
        - resource ex. `dfareporting.campaigns`
        - single method ex. `dfareporting.campaigns.insert`
    :param version: API version
    :param service_name: name which will be used for operators ex. `MarketingCampaigns`
    :param object_name: name used in operator class name, ex `Campaign` will be used
        in `MarketingCampaignsListCampaign`
    :param file_prefix: optional prefix for the operators file
    :param class_prefix: optional prefix for the operator class
    :param methods: optional list of methods for which operators should be generated
    """
