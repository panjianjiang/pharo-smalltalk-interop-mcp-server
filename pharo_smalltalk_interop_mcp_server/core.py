"""Core functions for Pharo MCP server without FastMCP decorators."""

import json
import os
from typing import Any

import httpx


class PharoInteropError(Exception):
    """Custom exception for Pharo interop errors."""

    pass


class PharoClient:
    """HTTP client for communicating with PharoSmalltalkInteropServer."""

    def __init__(self, host: str = "localhost", port: int | None = None):
        if port is None:
            port = int(os.getenv("PHARO_SIS_PORT", "8086"))
        self.base_url = f"http://{host}:{port}"
        self.client = httpx.Client(timeout=30.0)

    def _make_request(
        self, method: str, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make HTTP request to Pharo server."""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = self.client.get(url, params=data)
            else:
                response = self.client.post(url, json=data)

            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"success": False, "error": f"Connection error: {e}"}
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP error {e.response.status_code}: {e.response.text}",
            }
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON response: {e}"}

    def evaluate(self, code: str) -> dict[str, Any]:
        """Evaluate Smalltalk expression."""
        data = {"code": code}
        return self._make_request("POST", "/eval", data)

    def get_class_source(self, class_name: str) -> dict[str, Any]:
        """Get source code of a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/get-class-source", data)

    def get_method_source(
        self, class_name: str, method_name: str, *, is_class_method: bool = False
    ) -> dict[str, Any]:
        """Get source code of a method.

        Args:
            class_name: Name of the class containing the method
            method_name: Name of the method to retrieve
            is_class_method: True for class-side methods, False for instance methods (default: False)

        Returns:
            dict: API response with success/error and result
        """
        data = {
            "class_name": class_name,
            "method_name": method_name,
            "is_class_method": str(is_class_method).lower(),
        }
        return self._make_request("GET", "/get-method-source", data)

    def search_classes_like(self, class_name_query: str) -> dict[str, Any]:
        """Find classes matching pattern."""
        data = {"class_name_query": class_name_query}
        return self._make_request("GET", "/search-classes-like", data)

    def search_methods_like(self, method_name_query: str) -> dict[str, Any]:
        """Find methods matching pattern."""
        data = {"method_name_query": method_name_query}
        return self._make_request("GET", "/search-methods-like", data)

    def search_implementors(self, selector: str) -> dict[str, Any]:
        """Get implementors of a selector."""
        data = {"method_name": selector}
        return self._make_request("GET", "/search-implementors", data)

    def search_references(self, program_symbol: str) -> dict[str, Any]:
        """Get references to a selector."""
        data = {"program_symbol": program_symbol}
        return self._make_request("GET", "/search-references", data)

    def export_package(self, package_name: str, path: str = "/tmp") -> dict[str, Any]:
        """Export package in Tonel format."""
        data = {"package_name": package_name, "path": path}
        return self._make_request("GET", "/export-package", data)

    def import_package(self, package_name: str, path: str = "/tmp") -> dict[str, Any]:
        """Import package from Tonel format."""
        data = {"package_name": package_name, "path": path}
        return self._make_request("GET", "/import-package", data)

    def run_package_test(self, package_name: str) -> dict[str, Any]:
        """Run tests for a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/run-package-test", data)

    def run_class_test(self, class_name: str) -> dict[str, Any]:
        """Run tests for a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/run-class-test", data)

    def list_packages(self) -> dict[str, Any]:
        """List all packages."""
        return self._make_request("GET", "/list-packages")

    def list_classes(self, package_name: str) -> dict[str, Any]:
        """List classes in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-classes", data)

    def get_class_comment(self, class_name: str) -> dict[str, Any]:
        """Get comment of a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/get-class-comment", data)

    def list_extended_classes(self, package_name: str) -> dict[str, Any]:
        """List extended classes in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-extended-classes", data)

    def list_methods(self, package_name: str) -> dict[str, Any]:
        """List methods in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-methods", data)

    def search_traits_like(self, pattern: str) -> dict[str, Any]:
        """Find traits matching pattern."""
        data = {"trait_name_query": pattern}
        return self._make_request("GET", "/search-traits-like", data)

    def search_references_to_class(self, class_name: str) -> dict[str, Any]:
        """Find references to a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/search-references-to-class", data)

    def install_project(
        self,
        project_name: str,
        repository_url: str,
        load_groups: str | None = None,
    ) -> dict[str, Any]:
        """Install a project using Metacello."""
        data = {"project_name": project_name, "repository_url": repository_url}
        if load_groups:
            data["load_groups"] = load_groups
        return self._make_request("GET", "/install-project", data)

    def read_screen(
        self,
        target_type: str = "world",
        capture_screenshot: bool = True,
    ) -> dict[str, Any]:
        """Read and inspect Pharo UI structure with screenshot."""
        data = {
            "target_type": target_type,
            "capture_screenshot": capture_screenshot,
        }
        return self._make_request("GET", "/read-screen", data)

    def get_settings(self) -> dict[str, Any]:
        """Retrieve current server configuration."""
        return self._make_request("GET", "/get-settings")

    def apply_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        """Modify server configuration dynamically."""
        data = {"settings": settings}
        return self._make_request("POST", "/apply-settings", data)

    def poll_transcript(self, since: int = 0) -> dict[str, Any]:
        """Return transcript entries recorded since the given sequence cursor.

        Response shape:
            {seq, text, dropped, entries}
        where `seq` is the new cursor to pass in on the next poll,
        `text` joins the new entries, and `dropped` reports how many
        older entries were evicted from the ring buffer before the
        cursor caught up.
        """
        data = {"since": str(since)}
        return self._make_request("GET", "/transcript/poll", data)

    def clear_transcript(self) -> dict[str, Any]:
        """Reset the transcript ring buffer and sequence cursor."""
        return self._make_request("POST", "/transcript/clear")

    def inspect_expression(self, expression: str) -> dict[str, Any]:
        """Evaluate `expression` and return the SisInspector tree of the result.

        Each row in the tree carries an integer `ref' into a server-side
        registry; pass it to `inspect_ref` to drill into that subobject
        without re-evaluating anything.
        """
        data = {"expression": expression}
        return self._make_request("POST", "/inspect/expression", data)

    def inspect_ref(self, ref: int) -> dict[str, Any]:
        """Look up the live object stored under `ref` and return its tree."""
        data = {"ref": str(int(ref))}
        return self._make_request("GET", "/inspect/ref", data)

    def compile_method(
        self,
        class_name: str,
        method_source: str,
        category: str | None = None,
        is_class_method: bool = False,
    ) -> dict[str, Any]:
        """Compile a method onto `class_name` (or its metaclass when
        `is_class_method` is true). Returns `{selector, class_name,
        is_class_method, category}`. The server handles Smalltalk
        escaping — pass the source verbatim."""
        data: dict[str, Any] = {
            "class_name": class_name,
            "method_source": method_source,
            "is_class_method": is_class_method,
        }
        if category is not None:
            data["category"] = category
        return self._make_request("POST", "/compile-method", data)

    def compile_class(
        self,
        class_name: str,
        package: str,
        superclass: str = "Object",
        tag: str | None = None,
        inst_vars: list[str] | None = None,
        class_vars: list[str] | None = None,
        class_inst_vars: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create or update a class via ShiftClassBuilder. Returns
        `{class_name, created}` where `created` is true on first
        install, false on update."""
        data: dict[str, Any] = {
            "class_name": class_name,
            "superclass": superclass,
            "package": package,
            "inst_vars": list(inst_vars or []),
            "class_vars": list(class_vars or []),
            "class_inst_vars": list(class_inst_vars or []),
        }
        if tag is not None:
            data["tag"] = tag
        return self._make_request("POST", "/compile-class", data)

    def remove_method(
        self,
        class_name: str,
        selector: str,
        *,
        is_class_method: bool = False,
    ) -> dict[str, Any]:
        """Remove a method from a class or its metaclass.

        Returns `{class_name, selector, is_class_method, existed, removed}`.
        Missing classes/selectors are reported as `existed=false` rather than
        raising transport errors.
        """
        data = {
            "class_name": class_name,
            "selector": selector,
            "is_class_method": is_class_method,
        }
        return self._make_request("POST", "/remove-method", data)

    def remove_class(self, class_name: str) -> dict[str, Any]:
        """Remove a class from the image.

        Returns `{class_name, existed, removed}` with missing classes treated
        as a no-op.
        """
        data = {"class_name": class_name}
        return self._make_request("POST", "/remove-class", data)

    def close(self):
        """Close the HTTP client."""
        self.client.close()


# Global client instance
_pharo_client = None


def get_pharo_client() -> PharoClient:
    """Get or create global Pharo client instance."""
    global _pharo_client
    if _pharo_client is None:
        _pharo_client = PharoClient()
    return _pharo_client


def interop_eval(code: str) -> dict[str, Any]:
    """
    Evaluate a Pharo Smalltalk expression with PharoSmalltalkInteropServer.

    Args:
        code: The Smalltalk code to evaluate

    Returns:
        API response with success/error and result
    """
    client = get_pharo_client()
    return client.evaluate(code)


def interop_get_class_source(class_name: str) -> dict[str, Any]:
    """Get source code of a class."""
    client = get_pharo_client()
    return client.get_class_source(class_name)


def interop_get_method_source(
    class_name: str, method_name: str, *, is_class_method: bool = False
) -> dict[str, Any]:
    """Get source code of a method."""
    client = get_pharo_client()
    return client.get_method_source(
        class_name, method_name, is_class_method=is_class_method
    )


def interop_search_classes_like(class_name_query: str) -> dict[str, Any]:
    """Find classes matching pattern."""
    client = get_pharo_client()
    return client.search_classes_like(class_name_query)


def interop_search_methods_like(method_name_query: str) -> dict[str, Any]:
    """Find methods matching pattern."""
    client = get_pharo_client()
    return client.search_methods_like(method_name_query)


def interop_search_implementors(selector: str) -> dict[str, Any]:
    """Get implementors of a selector."""
    client = get_pharo_client()
    return client.search_implementors(selector)


def interop_search_references(program_symbol: str) -> dict[str, Any]:
    """Get references to a selector."""
    client = get_pharo_client()
    return client.search_references(program_symbol)


def interop_export_package(package_name: str, path: str = "/tmp") -> dict[str, Any]:
    """Export package in Tonel format."""
    client = get_pharo_client()
    return client.export_package(package_name, path)


def interop_import_package(package_name: str, path: str = "/tmp") -> dict[str, Any]:
    """Import package from specified path."""
    client = get_pharo_client()
    return client.import_package(package_name, path)


def interop_run_package_test(package_name: str) -> dict[str, Any]:
    """Run tests for a package."""
    client = get_pharo_client()
    return client.run_package_test(package_name)


def interop_run_class_test(class_name: str) -> dict[str, Any]:
    """Run tests for a class."""
    client = get_pharo_client()
    return client.run_class_test(class_name)


def interop_list_packages() -> dict[str, Any]:
    """List all packages."""
    client = get_pharo_client()
    return client.list_packages()


def interop_list_classes(package_name: str) -> dict[str, Any]:
    """List classes in a package."""
    client = get_pharo_client()
    return client.list_classes(package_name)


def interop_get_class_comment(class_name: str) -> dict[str, Any]:
    """Get comment of a class."""
    client = get_pharo_client()
    return client.get_class_comment(class_name)


def interop_list_extended_classes(package_name: str) -> dict[str, Any]:
    """List extended classes in a package."""
    client = get_pharo_client()
    return client.list_extended_classes(package_name)


def interop_list_methods(package_name: str) -> dict[str, Any]:
    """List methods in a package."""
    client = get_pharo_client()
    return client.list_methods(package_name)


def interop_search_traits_like(pattern: str) -> dict[str, Any]:
    """Find traits matching pattern."""
    client = get_pharo_client()
    return client.search_traits_like(pattern)


def interop_search_references_to_class(class_name: str) -> dict[str, Any]:
    """Find references to a class."""
    client = get_pharo_client()
    return client.search_references_to_class(class_name)


def interop_install_project(
    project_name: str, repository_url: str, load_groups: str | None = None
) -> dict[str, Any]:
    """Install a project using Metacello."""
    client = get_pharo_client()
    return client.install_project(project_name, repository_url, load_groups)


def interop_read_screen(
    target_type: str = "world",
    capture_screenshot: bool = True,
) -> dict[str, Any]:
    """Read and inspect Pharo UI structure with screenshot."""
    client = get_pharo_client()
    return client.read_screen(target_type, capture_screenshot)


def interop_get_settings() -> dict[str, Any]:
    """Retrieve current server configuration."""
    client = get_pharo_client()
    return client.get_settings()


def interop_apply_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """Modify server configuration dynamically."""
    client = get_pharo_client()
    return client.apply_settings(settings)


def interop_poll_transcript(since: int = 0) -> dict[str, Any]:
    """Return transcript entries recorded since the given sequence cursor."""
    client = get_pharo_client()
    return client.poll_transcript(since)


def interop_clear_transcript() -> dict[str, Any]:
    """Reset the transcript ring buffer and sequence cursor."""
    client = get_pharo_client()
    return client.clear_transcript()


def interop_inspect_expression(expression: str) -> dict[str, Any]:
    """Inspect a live Smalltalk value and return a drill-down tree."""
    client = get_pharo_client()
    return client.inspect_expression(expression)


def interop_inspect_ref(ref: int) -> dict[str, Any]:
    """Drill into a previously-inspected object by its server-side ref."""
    client = get_pharo_client()
    return client.inspect_ref(ref)


def interop_compile_method(
    class_name: str,
    method_source: str,
    category: str | None = None,
    is_class_method: bool = False,
) -> dict[str, Any]:
    """Compile a method onto a class (or its metaclass) without
    Smalltalk-string escaping on the caller side."""
    client = get_pharo_client()
    return client.compile_method(
        class_name,
        method_source,
        category=category,
        is_class_method=is_class_method,
    )


def interop_compile_class(
    class_name: str,
    package: str,
    superclass: str = "Object",
    tag: str | None = None,
    inst_vars: list[str] | None = None,
    class_vars: list[str] | None = None,
    class_inst_vars: list[str] | None = None,
) -> dict[str, Any]:
    """Create or update a class via ShiftClassBuilder."""
    client = get_pharo_client()
    return client.compile_class(
        class_name,
        package=package,
        superclass=superclass,
        tag=tag,
        inst_vars=inst_vars,
        class_vars=class_vars,
        class_inst_vars=class_inst_vars,
    )


def interop_remove_method(
    class_name: str,
    selector: str,
    *,
    is_class_method: bool = False,
) -> dict[str, Any]:
    """Remove a method from a class or its metaclass."""
    client = get_pharo_client()
    return client.remove_method(
        class_name, selector, is_class_method=is_class_method
    )


def interop_remove_class(class_name: str) -> dict[str, Any]:
    """Remove a class from the image."""
    client = get_pharo_client()
    return client.remove_class(class_name)
