'''
Returns json schema
'''

class Schema(object):

    def psconfig_pscheduler_json_schema(self):

        raw_json = {
            "id": "http://www.perfsonar.net/psconfig-pscheduler-agent-schema#",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "pSConfig pScheduler Agent Schema",
            "description": "Schema for pSConfig pScheduler agent configuration file. This is the file that tells the agent what pSConfig files to download and controls basic behaviors of agent script.",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "remotes": {
                    "type": "array",
                    "items": {
                        "$ref": "#/pSConfig/RemoteSpecification"
                    },
                    "description": "List of remote pSConfig JSON files to to read"
                },
                "pscheduler-assist-server": {
                    "$ref": "#/pSConfig/URLHostPort",
                    "description": "URL of pScheduler assist server to use when validating and submitting requests. Default is the local pScheduler server."
                },
                "pscheduler-fail-attempts": {
                    "$ref": "#/pSConfig/Cardinal",
                    "description": "The number of attempts to contact the pscheduler-assist-server before giving-up for time specified by check-interval. Default is 5."
                },
                "match-addresses": {
                    "type": "array",
                    "items": {
                        "$ref": "#/pSConfig/Host"
                    },
                    "description": "List of IP addresses and/or hostnames to use when determining which tests this agent should configure. Default is all the addresses found on interfaces on this host."
                },
                "pscheduler-bind-map": {
                    "$ref": "#/pSConfig/AddressMap",
                    "description": "Maps a remote pscheduler address to the local address to use when trying to communicate with aforementioned remote address. Remote address is key and local address is value. Special key _default is used if no address matches. If no _default and no remote address matches a key then uses local routing table."
                },
                "include-directory": {
                    "type": "string",
                    "description": "Directory with local pSConfig files to be processed. Default is /etc/psconfig/pscheduler.d"
                },
                "archive-directory": {
                    "type": "string",
                    "description": "Directory with default archives to be added to all tasks. Default is /etc/psconfig/archives.d"
                },
                "transform-directory": {
                    "type": "string",
                    "description": "Directory with default transformations to apply to JSON processed by agent. Default is /etc/psconfig/transforms.d"
                },
                "requesting-agent-file": {
                    "type": "string",
                    "description": "Path to file defining JSON to be used as the requesting-agent data source in address classes. Default is /etc/psconfig/requesting-agent.json. If file does not exist, a default set of JSON will be generated based on local host interfaces."
                },
                "client-uuid-file": {
                    "type": "string",
                    "description": "Path to file with UUID for this client. Default is /var/lib/psconfid/client-uuid"
                },
                "pscheduler-tracker-file": {
                    "type": "string",
                    "description": "Path to file tracking pscheduler servers used in building tasks. Default is /var/lib/psconfig/psc_tracker"
                },
                "check-interval": {
                    "$ref": "#/pSConfig/Duration",
                    "description": "ISO8601 indicating how often to check for changes to the pSConfig files in remotes and includes. Default is 1 hour ('PT1H')."
                },
                "check-config-interval": {
                    "$ref": "#/pSConfig/Duration",
                    "description": "ISO8601 indicating how often to check for changes to the local configuration files. This includes this config file, the includes directory, the requesting-agent file and the archives directory. Default is 1 minute ('PT60S')."
                },
                "task-min-ttl": {
                    "$ref": "#/pSConfig/Duration",
                    "description": "The minimum expiration of new tasks created by this agent. Default is 24 hours (PT24H)."
                },
                "task-min-runs": {
                    "$ref": "#/pSConfig/Cardinal",
                    "description": "The minimum number of runs a task must have. If this number of runs exceeds the task-min-ttl, then the time required for these runs will be the expiration. If it is less than task-min-ttl, then task-min-ttl will be used. Default is 2 runs."
                },
                "task-renewal-fudge-factor": {
                    "$ref": "#/pSConfig/Probability",
                    "description": "The percentage of time before a task expires that a new task will be created. Default is 25% (specified as .25)"
                },
                "disable-cache": {
                    "type": "boolean",
                    "description": "Boolean indicating that if a template cannot be accessed or is invalid, a cached version should NOT be used if exists. The cache prevents inaccessible or invalid templates from causing tasks to be deleted immediately. Items in cache expire, so it will only protect tasks from deletion while cache entry is valid. Default is false."
                },
                "cache-directory": {
                    "type": "string",
                    "description": "Path to directory where templates should be cached. Default is /var/lib/perfsonar/psconfig/template_cache."
                },
                "cache-expires": {
                    "$ref": "#/pSConfig/Duration",
                    "description": "ISO8601 indicating how long to cache templates. Default is 1 day (P1D)."
                }
            },
            "pSConfig": {
                "AddressMap": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-zA-Z0-9:._\\-]+$": {
                            "$ref": "#/pSConfig/Host"
                        }
                    },
                    "additionalProperties": False
                },
                "Cardinal": {
                    "type": "integer",
                    "minimum": 1
                },
                "Duration": {
                    "type": "string",
                    "pattern": "^P(?:\\d+(?:\\.\\d+)?W)?(?:\\d+(?:\\.\\d+)?D)?(?:T(?:\\d+(?:\\.\\d+)?H)?(?:\\d+(?:\\.\\d+)?M)?(?:\\d+(?:\\.\\d+)?S)?)?$",
                    "x-invalid-message": "'%s' is not a valid ISO 8601 duration."
                },
                "Host": {
                    "anyOf": [
                        {
                            "$ref": "#/pSConfig/HostName"
                        },
                        {
                            "$ref": "#/pSConfig/IPAddress"
                        }
                    ]
                },
                "HostName": {
                    "type": "string",
                    "format": "hostname"
                },
                "HostNamePort": {
                    "type": "string",
                    "pattern": "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])(:[0-9]+)?$"
                },
                "IPAddress": {
                    "oneOf": [
                        {
                            "type": "string",
                            "format": "ipv4"
                        },
                        {
                            "type": "string",
                            "format": "ipv6"
                        }
                    ]
                },
                "IPv6RFC2732": {
                    "type": "string",
                    "pattern": "^\\[(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\\](:[0-9]+)?$"
                },
                "JQTransformSpecification": {
                    "type": "object",
                    "properties": {
                        "script": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            ]
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "script"
                    ]
                },
                "Probability": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0
                },
                "RemoteSpecification": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "format": "uri",
                            "description": "URL of psconfig file to read"
                        },
                        "configure-archives": {
                            "type": "boolean",
                            "description": "If true will use archives specified in remote psconfig file. Default it false."
                        },
                        "transform": {
                            "$ref": "#/pSConfig/JQTransformSpecification",
                            "description": "JQ script to transform downloaded pSConfig JSON"
                        },
                        "bind-address": {
                            "$ref": "#/pSConfig/Host",
                            "description": "Local address to use when downloading JSON. Default is to let local routing tables choose."
                        },
                        "ssl-ca-file": {
                            "type": "string",
                            "description": "A certificate authority (CA) file used to verify server SSL certificate when using https."
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "url"
                    ]
                },
                "URLHostPort": {
                    "anyOf": [
                        {
                            "$ref": "#/pSConfig/HostNamePort"
                        },
                        {
                            "$ref": "#/pSConfig/IPv6RFC2732"
                        }
                    ]
                }
            }
        }
        return raw_json
