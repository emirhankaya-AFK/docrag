import semver
from typing import Dict, Any, Optional

class VersionManagerService:
    @staticmethod
    def compare_versions(v1: str, v2: str) -> int:
        """
        Compares two semantic versions. Returns -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2.
        """
        # Clean versions (remove leading v, etc.)
        c1 = VersionManagerService._clean_version(v1)
        c2 = VersionManagerService._clean_version(v2)
        
        try:
            sem1 = semver.VersionInfo.parse(c1)
            sem2 = semver.VersionInfo.parse(c2)
            return sem1.compare(sem2)
        except Exception:
            # Fallback string split compare if not strictly semver
            try:
                p1 = [int(x) for x in c1.split(".") if x.isdigit()]
                p2 = [int(x) for x in c2.split(".") if x.isdigit()]
                for a, b in zip(p1, p2):
                    if a < b: return -1
                    if a > b: return 1
                return 0
            except Exception:
                return 0

    @staticmethod
    def is_method_deprecated(method_added_ver: Optional[str], current_ver: str, deprecation_ver: Optional[str] = None) -> Dict[str, Any]:
        """
        Determines deprecation status based on version numbers.
        """
        is_deprecated = False
        warning = None
        
        if deprecation_ver and current_ver:
            cmp_val = VersionManagerService.compare_versions(current_ver, deprecation_ver)
            if cmp_val >= 0:
                is_deprecated = True
                warning = f"This method was deprecated in version {deprecation_ver} and you are running {current_ver}."
                
        return {
            "is_deprecated": is_deprecated,
            "warning": warning
        }

    @staticmethod
    def _clean_version(ver: str) -> str:
        ver = ver.strip().lower()
        if ver.startswith("v"):
            ver = ver[1:]
        # Ensure at least 3 parts (major.minor.patch)
        parts = ver.split(".")
        while len(parts) < 3:
            parts.append("0")
        return ".".join(parts[:3])
