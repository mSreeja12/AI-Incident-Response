categories = {
    "database": [
        "sql",
        "database",
        "db",
        "query",
        "connection timeout",
        "mongodb",
        "mysql",
        "postgres",
        "deadlock"
    ],

    "authentication": [
        "login failed",
        "unauthorized",
        "token",
        "auth",
        "password",
        "jwt",
        "access denied"
    ],

    "api": [
        "503",
        "502",
        "500",
        "gateway",
        "api error",
        "service unavailable",
        "bad gateway",
        "endpoint failure"
    ],

    "deployment": [
        "docker",
        "deployment",
        "deploy",
        "rollback",
        "release failed",
        "crashloop",
        "container restart"
    ],

    "infrastructure": [
        "cpu",
        "memory",
        "disk",
        "latency",
        "server",
        "pod crashed",
        "kubernetes",
        "node failure",
        "network timeout"
    ],

    "security": [
        "attack",
        "malware",
        "suspicious",
        "breach",
        "unknown ip",
        "ddos",
        "intrusion"
    ]
}


def classify_log(log):

    log = log.lower()

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in log:
                return category

    return "general incident"


def severity_prediction(log):

    log = log.lower()

    critical_keywords = [
        "critical",
        "shutdown",
        "outage",
        "service unavailable",
        "503",
        "crashed",
        "down",
        "data loss"
    ]

    high_keywords = [
        "timeout",
        "502",
        "500",
        "latency",
        "error",
        "failed",
        "connection refused"
    ]

    medium_keywords = [
        "warning",
        "retry",
        "slow response",
        "degraded"
    ]

    for word in critical_keywords:
        if word in log:
            return "Critical"

    for word in high_keywords:
        if word in log:
            return "High"

    for word in medium_keywords:
        if word in log:
            return "Medium"

    return "Low"