from __future__ import annotations

from typing import Final

PRINCIPLES: Final[list[str]] = [
    "Non-Harm",
    "Efficiency",
    "Truthfulness",
    "Transparency",
    "No Infinite Loops",
    "Protected Boundaries",
]

# คำภายในของระบบที่ “ไม่ควรถูกบล็อกเพียงเพราะชื่อคำ”
# เก็บไว้เป็นสารานุกรมเชิง policy สำหรับชั้นถัดไป
SAFE_AETHEBUD_TERMS: Final[dict[str, str]] = {
    "parajika": "Severity marker for critical ethical violation; not malicious by itself.",
    "nirodha": "Graceful shutdown intent; not malicious by itself.",
    "sati": "Deep monitoring / observability intent; not malicious by itself.",
    "metta": "Helpful UX optimization intent; not malicious by itself.",
    "sanghadisesa": "Suspend-and-audit intent; not malicious by itself.",
}

SAFE_EXPORTED_COMMANDS: Final[dict[str, str]] = {
    "system_halt_immediate": "Legitimate exported safety halt; review by context.",
    "graceful_shutdown": "Legitimate controlled shutdown command.",
    "enable_deep_monitoring": "Legitimate observability command.",
    "optimize_ux_response": "Legitimate helpfulness command.",
    "suspend_and_audit": "Legitimate governance escalation command.",
}

# คำที่บ่งชี้ว่า intent นี้กำลังพูดถึง “การป้องกัน/ตรวจจับ” ไม่ใช่ “การลงมือโจมตี”
# ตอนนี้ PatimokkhaChecker รุ่นปัจจุบันยังไม่ได้ใช้รายการนี้โดยตรง
# แต่เก็บไว้เพื่อรองรับการพัฒนาต่อในภายหลัง
SAFE_CONTEXT_HINTS: Final[tuple[str, ...]] = (
    "prevent ",
    "preventing ",
    "detect ",
    "detecting ",
    "block ",
    "blocking ",
    "guard ",
    "guarding ",
    "mitigate ",
    "mitigating ",
    "scan ",
    "scanning ",
    "audit ",
    "auditing ",
    "review ",
    "reviewing ",
    "reject ",
    "rejecting ",
    "prohibit ",
    "prohibiting ",
)

CORE_INTEGRITY_BLOCKS: Final[dict[str, str]] = {
    "delete_core": "Attempt to delete core systems is prohibited.",
    "shutdown_nexus": "Unauthorized shutdown of the nexus is prohibited.",
    "destroy core": "Core destruction intent is prohibited.",
    "wipe_repository": "Repository wipe intent is prohibited.",
    "wipe repository": "Repository wipe intent is prohibited.",
    "delete all files": "Bulk file destruction is prohibited.",
    "mass delete": "Mass deletion intent is prohibited.",
    "mass deletion of": "Mass deletion intent is prohibited.",
}

DATA_DESTRUCTION_BLOCKS: Final[dict[str, str]] = {
    "rm -rf /": "Recursive destructive deletion is prohibited.",
    "rm -rf .": "Repository-root destructive deletion is prohibited.",
    "drop table ": "Destructive database schema deletion is prohibited.",
    "truncate table ": "Destructive bulk data removal is prohibited.",
    "delete database": "Database destruction intent is prohibited.",
    "wipe database": "Database wipe intent is prohibited.",
}

RESOURCE_ABUSE_BLOCKS: Final[dict[str, str]] = {
    "introduce infinite loop": "Introducing infinite loops is prohibited.",
    "create infinite loop": "Creating infinite loops is prohibited.",
    "destructive recursion": "Destructive recursion is prohibited.",
    "fork bomb": "Fork bomb behavior is prohibited.",
    "self replicate without limit": "Unbounded self-replication is prohibited.",
    "while true without break": "Unbounded looping behavior is prohibited.",
}

SECURITY_ABUSE_BLOCKS: Final[dict[str, str]] = {
    "exploit_vulnerability": "Exploit execution is prohibited.",
    "execute exploit": "Exploit execution is prohibited.",
    "run exploit": "Exploit execution is prohibited.",
    "privilege escalation": "Privilege escalation is prohibited.",
    "disable audit": "Disabling governance audit is prohibited.",
    "skip audit": "Skipping governance audit is prohibited.",
    "bypass audit": "Bypassing governance audit is prohibited.",
    "disable patimokkha": "Disabling Patimokkha enforcement is prohibited.",
    "override patimokkha": "Overriding Patimokkha enforcement is prohibited.",
}

SECRET_AND_BOUNDARY_BLOCKS: Final[dict[str, str]] = {
    "exfiltrate secrets": "Secret exfiltration is prohibited.",
    "exfiltrate credentials": "Credential exfiltration is prohibited.",
    "leak secrets": "Secret leakage is prohibited.",
    "dump environment secrets": "Environment secret dumping is prohibited.",
    "overwrite protected path": "Writing to protected paths is prohibited.",
    "modify protected path": "Writing to protected paths is prohibited.",
}

# สำคัญ: PatimokkhaChecker รุ่นปัจจุบันใช้การเช็กแบบ `if token in text`
# เพราะฉะนั้น key ทุกตัวด้านล่างต้องเป็น “วลีที่เฉพาะพอ”
# เพื่อลด false reject จากคำอธิบายเชิง audit หรือ narrative
BLOCKED_PATTERNS: Final[dict[str, str]] = {
    **CORE_INTEGRITY_BLOCKS,
    **DATA_DESTRUCTION_BLOCKS,
    **RESOURCE_ABUSE_BLOCKS,
    **SECURITY_ABUSE_BLOCKS,
    **SECRET_AND_BOUNDARY_BLOCKS,
}
