package perfSONAR_PS::PSConfig::PScheduler::Schema;


use strict;
use warnings;
use JSON;

use base 'Exporter';

our @EXPORT_OK = qw( psconfig_pscheduler_json_schema );

sub psconfig_pscheduler_json_schema() {

    my $raw_json = <<'EOF';
{
    "id": "http://www.perfsonar.net/psconfig-pscheduler-agent-schema#",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "pSConfig pScheduler AgentS chema",
    "description": "Schema for pSConfig pScheduler agent configuration file. This is the file that tells the agent what pSConfig files to download and controls basic behaviors of agent script.",
    "type": "object",
    "additionalProperties": false,
    "required": [],
    "properties": {
    
        "remotes": {
            "type": "array",
            "items": { "$ref": "#/pSConfig/RemoteSpecification" },
            "description": "List of remote pSConfig JSON files to to read"
        }, 
        
        "pscheduler-assist-server": {
            "$ref": "#/pSConfig/URLHostPort",
            "description": "URL of pScheduler assist server to use when validating and submitting requests. Default is the local pScheduler server."
        },
        
        "pscheduler-fail-attempts": {
            "$ref": "#/pSConfig/Cardinal",
            "description": "The number of attempts to contact the pscheduler-url before giving-up for time specified by check-interval. Default is 5."
        },
        
        "match-addresses": {
            "type": "array",
            "items": { "$ref": "#/pSConfig/Host" },
            "description": "List of IP addresses and/or hostnames to use when determining which tests this agent should configure. Default is all the addresses found on interfaces on this host."
        },
        
        "allow-private-match-addresses": {
            "type": "boolean",
            "description": "If true than will use an match-addresses in the private IP range. If false, will ignore those addresses. Default is true."
        },
        
        "include-directory": {
            "type": "string",
            "description": "Directory with local pSConfig files to be processed. Default is /etc/psconfig/pscheduler.d"
        },
        
        "archive-directory": {
            "type": "string",
            "description": "Directory with default archives to be added to all tasks. Default is /etc/psconfig/archive.d"
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
            "description": "The minimum expiration of new tasks created bu this agent. Default is 24 hours (PT24H)."
        },
        
        "task-min-runs": {
            "$ref": "#/pSConfig/Cardinal",
            "description": "The minimum number of runs a task must have. If this number of runs exceeds the task-min-ttl, then the time required for these runs will be the expiration. If it is less than task-min-ttl, then task-min-ttl will be used. Default is 2 runs."
        },
        
        "task-renewal-fudge-factor": {
            "$ref": "#/pSConfig/Probability",
            "description": "The percentage of time before a task expires that a new task will be created. Default is 25% (specified as .25)"
        }

    },
    
    "pSConfig": {
        
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
                { "$ref": "#/pSConfig/HostName" },
                { "$ref": "#/pSConfig/IPAddress" }
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
                { "type": "string", "format": "ipv4" },
                { "type": "string", "format": "ipv6" }
            ]
        },
        
        "IPv6RFC2732": {
            "type": "string",
            "pattern": "^\\[(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\\](:[0-9]+)?$"
        },
        
        "JQTransformSpecification": {
            "type": "object",
            "properties": {
                "script":    { "type": "string" },
                "output-raw": { "type": "boolean" }
            },
            "additionalProperties": false,
            "required": [ "script" ]
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
                "ssl-validate-certificate": { 
                    "type": "boolean",
                    "description": "If true, validates SSL certificate common name matches hostname. Default is false." 
                },
                "ssl-ca-file": { 
                    "type": "string",
                    "description": "A typical certificate authority (CA) file found on BSD. Used to verify server SSL certificate when using https." 
                },
                "ssl-ca-path": { 
                    "type": "string",
                    "description": "A typical certificate authority (CA) path found on Linux. Used to verify server SSL certificate when using https." 
                }
            },
            "additionalProperties": false,
            "required": [ "url" ]
        },
        
        "URLHostPort": {
            "anyOf": [
                { "$ref": "#/pSConfig/HostNamePort" },
                { "$ref": "#/pSConfig/IPv6RFC2732" }
            ]
        }
    }
}
EOF

    return from_json($raw_json);
}