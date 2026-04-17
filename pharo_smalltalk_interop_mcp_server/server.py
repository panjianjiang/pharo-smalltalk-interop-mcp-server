"""FastMCP server for Pharo Smalltalk evaluation."""

from typing import Annotated, Any

from fastmcp import Context, FastMCP
from pydantic import Field

from .core import (
    interop_apply_settings,
    interop_clear_transcript,
    interop_compile_class,
    interop_compile_method,
    interop_eval,
    interop_export_package,
    interop_get_class_comment,
    interop_get_class_source,
    interop_get_method_source,
    interop_get_settings,
    interop_import_package,
    interop_inspect_expression,
    interop_inspect_ref,
    interop_install_project,
    interop_list_classes,
    interop_list_extended_classes,
    interop_list_methods,
    interop_list_packages,
    interop_poll_transcript,
    interop_read_screen,
    interop_remove_class,
    interop_remove_method,
    interop_run_class_test,
    interop_run_package_test,
    interop_search_classes_like,
    interop_search_implementors,
    interop_search_methods_like,
    interop_search_references,
    interop_search_references_to_class,
    interop_search_traits_like,
)

mcp = FastMCP("pharo-smalltalk-interop-mcp-server")


@mcp.tool("eval")
def eval_code(
    _: Context,
    code: Annotated[str, Field(description="The Smalltalk code to evaluate")],
) -> dict[str, Any]:
    """
    Evaluate a Pharo Smalltalk expression with PharoSmalltalkInteropServer.

    Args:
        code: The Smalltalk code to evaluate

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": any} - result contains the evaluation result
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_eval(code)


@mcp.tool("get_class_source")
def get_class_source(
    _: Context,
    class_name: Annotated[
        str, Field(description="The name of the class to retrieve source for")
    ],
) -> dict[str, Any]:
    """
    Get the source code of a Smalltalk class.

    Args:
        class_name: The name of the class to retrieve source for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains the class source code
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_get_class_source(class_name)


@mcp.tool("get_method_source")
def get_method_source(
    _: Context,
    class_name: Annotated[
        str, Field(description="The name of the class containing the method")
    ],
    method_name: Annotated[
        str, Field(description="The name of the method to retrieve source for")
    ],
    is_class_method: Annotated[
        bool,
        Field(
            description="Set to True for class-side methods, False for instance methods (default: False)"
        ),
    ] = False,
) -> dict[str, Any]:
    """
    Get the source code of a specific method in a class.

    Args:
        class_name: The name of the class containing the method
        method_name: The name of the method to retrieve source for
        is_class_method: True for class-side methods, False for instance methods (default: False)

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains the method source code
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_get_method_source(
        class_name, method_name, is_class_method=is_class_method
    )


@mcp.tool("get_class_comment")
def get_class_comment(
    _: Context,
    class_name: Annotated[
        str, Field(description="The name of the class to retrieve comment for")
    ],
) -> dict[str, Any]:
    """
    Get the comment of a Smalltalk class.

    Args:
        class_name: The name of the class to retrieve comment for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains the class comment
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_get_class_comment(class_name)


@mcp.tool("search_classes_like")
def search_classes_like(
    _: Context,
    class_name_query: Annotated[
        str, Field(description="The pattern to search for in class names")
    ],
) -> dict[str, Any]:
    """
    Find classes matching a pattern.

    Args:
        class_name_query: The pattern to search for in class names

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of matching class names
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_classes_like(class_name_query)


@mcp.tool("search_methods_like")
def search_methods_like(
    _: Context,
    method_name_query: Annotated[
        str, Field(description="The pattern to search for in method names")
    ],
) -> dict[str, Any]:
    """
    Find methods matching a pattern.

    Args:
        method_name_query: The pattern to search for in method names

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of matching method names
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_methods_like(method_name_query)


@mcp.tool("search_implementors")
def search_implementors(
    _: Context,
    method_name: Annotated[
        str, Field(description="The method name to find implementors for")
    ],
) -> dict[str, Any]:
    """
    Get all implementors of a method selector.

    Args:
        method_name: The method name to find implementors for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[dict]} - result contains list of implementors
          Each implementor: {"class": str, "method": str, "package": str}
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_implementors(method_name)


@mcp.tool("search_references")
def search_references(
    _: Context,
    method_name_or_symbol: Annotated[
        str, Field(description="The method name or symbol to find references for")
    ],
) -> dict[str, Any]:
    """
    Get all references to a method selector or a symbol.

    Args:
        method_name_or_symbol: The method name to find references for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[dict]} - result contains list of references
          Each reference: {"class": str, "method": str, "package": str}
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_references(method_name_or_symbol)


@mcp.tool("list_packages")
def list_packages(_: Context) -> dict[str, Any]:
    """
    Get list of all packages.

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of all package names
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_list_packages()


@mcp.tool("list_classes")
def list_classes(
    _: Context,
    package_name: Annotated[str, Field(description="The name of the package")],
) -> dict[str, Any]:
    """
    Get list of classes in a package.

    Args:
        package_name: The name of the package

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of class names in package
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_list_classes(package_name)


@mcp.tool("export_package")
def export_package(
    _: Context,
    package_name: Annotated[
        str, Field(description="The name of the package to export")
    ],
    path: Annotated[
        str, Field(description="The path where to export the package")
    ] = "/tmp",
) -> dict[str, Any]:
    """
    Export a package in Tonel format.

    Args:
        package_name: The name of the package to export
        path: The path where to export the package (default: /tmp)

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains export success message with path
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_export_package(package_name, path)


@mcp.tool("import_package")
def import_package(
    _: Context,
    package_name: Annotated[
        str, Field(description="The name of the package to import")
    ],
    path: Annotated[
        str, Field(description="The path to the package file to import")
    ] = "/tmp",
) -> dict[str, Any]:
    """
    Import a package from specified path.

    Args:
        package_name: The name of the package to import
        path: The path to the package file to import (default: /tmp)

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains import success message
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_import_package(package_name, path)


@mcp.tool("run_package_test")
def run_package_test(
    _: Context,
    package_name: Annotated[
        str, Field(description="The package name to run tests for")
    ],
) -> dict[str, Any]:
    """
    Run tests for a package.

    Args:
        package_name: The package name to run tests for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains test results summary
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_run_package_test(package_name)


@mcp.tool("run_class_test")
def run_class_test(
    _: Context,
    class_name: Annotated[str, Field(description="The class name to run tests for")],
) -> dict[str, Any]:
    """
    Run tests for a class.

    Args:
        class_name: The class name to run tests for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains test results summary
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_run_class_test(class_name)


@mcp.tool("list_extended_classes")
def list_extended_classes(
    _: Context,
    package_name: Annotated[str, Field(description="The name of the package")],
) -> dict[str, Any]:
    """
    Get list of extended classes in a package.

    Args:
        package_name: The name of the package

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of extended class names
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_list_extended_classes(package_name)


@mcp.tool("list_methods")
def list_methods(
    _: Context,
    package_name: Annotated[str, Field(description="The name of the package")],
) -> dict[str, Any]:
    """
    Get list of methods in a package.

    Args:
        package_name: The name of the package

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of method signatures
          Each method: "ClassName>>#methodName"
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_list_methods(package_name)


@mcp.tool("search_traits_like")
def search_traits_like(
    _: Context,
    trait_name_query: Annotated[
        str, Field(description="The pattern to search for in trait names")
    ],
) -> dict[str, Any]:
    """
    Find traits matching a pattern.

    Args:
        trait_name_query: The pattern to search for in trait names

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[str]} - result contains list of matching trait names
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_traits_like(trait_name_query)


@mcp.tool("search_references_to_class")
def search_references_to_class(
    _: Context,
    class_name: Annotated[
        str, Field(description="The name of the class to find references for")
    ],
) -> dict[str, Any]:
    """
    Find references to a class.

    Args:
        class_name: The name of the class to find references for

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": list[dict]} - result contains list of class references
          Each reference: {"package": str, "class": str, "method": str}
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_search_references_to_class(class_name)


@mcp.tool("install_project")
def install_project(
    _: Context,
    project_name: Annotated[
        str, Field(description="The name of the project to install")
    ],
    repository_url: Annotated[
        str, Field(description="The repository URL for the project")
    ],
    load_groups: Annotated[
        str | None, Field(description="Comma-separated list of groups to load")
    ] = None,
) -> dict[str, Any]:
    """
    Install a project using Metacello.

    Args:
        project_name: The name of the project to install
        repository_url: The repository URL for the project
        load_groups: Comma-separated list of groups to load (optional)

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains installation success message
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_install_project(project_name, repository_url, load_groups)


@mcp.tool("read_screen")
def read_screen(
    _: Context,
    target_type: Annotated[
        str,
        Field(
            description="UI type to inspect: 'world' (morphs), 'spec' (windows), or 'roassal' (visualizations)"
        ),
    ] = "world",
    capture_screenshot: Annotated[
        bool, Field(description="Include PNG screenshot in response")
    ] = True,
) -> dict[str, Any]:
    """
    Comprehensive UI screen reader for debugging Pharo interfaces.

    Captures screenshot and extracts complete UI structure for World morphs, Spec presenters, and Roassal visualizations.

    Args:
        target_type: 'world' for morphs, 'spec' for Spec windows, 'roassal' for visualizations
        capture_screenshot: Include PNG screenshot in response (default: true)

    Returns:
        dict: UI structure and metrics
        - screenshot: Path to PNG file in /tmp/ (if capture_screenshot=true)
        - target_type: Which UI type was inspected
        - structure: Complete UI hierarchy data
        - summary: Human-readable description
    """
    return interop_read_screen(target_type, capture_screenshot)


@mcp.tool("get_settings")
def get_settings(_: Context) -> dict[str, Any]:
    """
    Retrieve current server configuration.

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": dict} - result contains current server settings
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_get_settings()


@mcp.tool("apply_settings")
def apply_settings(
    _: Context,
    settings: Annotated[
        dict[str, Any], Field(description="Settings dictionary to apply to the server")
    ],
) -> dict[str, Any]:
    """
    Modify server configuration dynamically.

    Args:
        settings: Dictionary containing server settings to modify

    Returns:
        dict: API response with success/error and result
        - Success: {"success": True, "result": str} - result contains confirmation message
        - Error: {"success": False, "error": str} - error contains error message
    """
    return interop_apply_settings(settings)


@mcp.tool("poll_transcript")
def poll_transcript(
    _: Context,
    since: Annotated[
        int,
        Field(
            description=(
                "Sequence cursor returned by the previous poll "
                "(use 0 for a full read-out)"
            ),
            ge=0,
        ),
    ] = 0,
) -> dict[str, Any]:
    """
    Return transcript entries recorded since the given cursor.

    The Pharo-side tee wraps Transcript and records every write into a
    capped ring buffer with a monotonically increasing sequence number.
    Callers poll with the last `seq` they saw; the response's `seq`
    becomes the next cursor.  `dropped` reports entries that rolled
    off the ring before the cursor could catch up.

    Args:
        since: Last-seen sequence cursor (0 = from the start of the ring).

    Returns:
        dict: {"success": True, "result": {"seq", "text", "entries", "dropped"}}.
    """
    return interop_poll_transcript(since)


@mcp.tool("clear_transcript")
def clear_transcript(_: Context) -> dict[str, Any]:
    """
    Reset the transcript ring buffer and sequence cursor to 0.

    Returns:
        dict: {"success": True, "result": {"seq": 0}}.
    """
    return interop_clear_transcript()


@mcp.tool("inspect_expression")
def inspect_expression(
    _: Context,
    expression: Annotated[
        str,
        Field(
            description=(
                "Smalltalk expression to evaluate; the result is registered "
                "in the server-side ref table and returned as a tree."
            )
        ),
    ],
) -> dict[str, Any]:
    """
    Evaluate EXPRESSION and return the SisInspector tree of its result.

    Each row in the tree carries an integer `ref` into a server-side
    IdentityDictionary so subsequent `inspect_ref` calls drill into the
    same live object without re-evaluating.  Indexable collections
    expose their elements under `indexable`; named slots come through
    under `inst_vars`.

    Args:
        expression: Smalltalk code that returns the object to inspect.

    Returns:
        dict: {"success": True, "result": <tree>}.
    """
    return interop_inspect_expression(expression)


@mcp.tool("inspect_ref")
def inspect_ref(
    _: Context,
    ref: Annotated[
        int,
        Field(
            description=(
                "Ref returned by an earlier `inspect_expression` / "
                "`inspect_ref` call; looks up the same live object."
            ),
            ge=0,
        ),
    ],
) -> dict[str, Any]:
    """
    Drill into a previously inspected object by its ref.

    Refs are registered during inspection and evicted LRU-style once
    the registry hits its cap (1024 entries).  If a ref is no longer
    valid you'll get a success=false response with a description.

    Args:
        ref: Integer ref carried in an earlier inspection tree row.

    Returns:
        dict: {"success": True, "result": <tree>}.
    """
    return interop_inspect_ref(ref)


@mcp.tool("compile_method")
def compile_method(
    _: Context,
    class_name: Annotated[
        str, Field(description="Target class name (e.g. 'OrderedCollection')")
    ],
    method_source: Annotated[
        str,
        Field(
            description=(
                "Full Smalltalk source of the method, including the "
                "selector header.  Pass verbatim — no escaping needed."
            )
        ),
    ],
    category: Annotated[
        str | None,
        Field(
            description=(
                "Method protocol / category.  Defaults to "
                "'as yet unclassified' when omitted."
            )
        ),
    ] = None,
    is_class_method: Annotated[
        bool,
        Field(description="True to compile on the metaclass (class-side)."),
    ] = False,
) -> dict[str, Any]:
    """
    Compile a single method onto a class (or its metaclass).

    Goes through the structured /compile-method endpoint so the source
    is never re-escaped into a Smalltalk string literal — quotes,
    backslashes, and newlines all travel as JSON.

    Returns:
        dict: {"success": True,
               "result": {"selector", "class_name",
                          "is_class_method", "category",
                          "overwritten", "previous_source?"}}.
        On compile failure: {"success": False, "error": {
            "description", "message_text", "source", "class_name",
            "is_class_method", "location?", "line?", "column?"
        }}.
    """
    return interop_compile_method(
        class_name,
        method_source,
        category=category,
        is_class_method=is_class_method,
    )


@mcp.tool("compile_class")
def compile_class(
    _: Context,
    class_name: Annotated[str, Field(description="New or existing class name.")],
    package: Annotated[
        str, Field(description="Package that owns the class (created if missing).")
    ],
    superclass: Annotated[
        str, Field(description="Superclass name; defaults to 'Object'.")
    ] = "Object",
    tag: Annotated[
        str | None,
        Field(description="Optional sub-package / tag label."),
    ] = None,
    inst_vars: Annotated[
        list[str] | None,
        Field(description="Named instance variables.  Order preserved."),
    ] = None,
    class_vars: Annotated[
        list[str] | None,
        Field(description="Shared (class-level) variables."),
    ] = None,
    class_inst_vars: Annotated[
        list[str] | None,
        Field(description="Metaclass-side instance variables."),
    ] = None,
) -> dict[str, Any]:
    """
    Create or update a class via ShiftClassBuilder.

    First call with a new name returns `created=true`; subsequent calls
    return `created=false` and re-shape the existing class to match the
    provided slots.

    Returns:
        dict: {"success": True, "result": {"class_name", "created"}}.
    """
    return interop_compile_class(
        class_name,
        package=package,
        superclass=superclass,
        tag=tag,
        inst_vars=inst_vars,
        class_vars=class_vars,
        class_inst_vars=class_inst_vars,
    )


@mcp.tool("remove_method")
def remove_method(
    _: Context,
    class_name: Annotated[
        str, Field(description="Class name that owns the method.")
    ],
    selector: Annotated[
        str, Field(description="Selector to remove, e.g. 'value' or 'at:put:'.")
    ],
    is_class_method: Annotated[
        bool,
        Field(
            description="True to remove the method from the metaclass (class-side)."
        ),
    ] = False,
) -> dict[str, Any]:
    """
    Remove a method from a class or its metaclass.

    Missing classes or selectors are reported as a successful no-op
    with `existed=false, removed=false`.

    Returns:
        dict: {"success": True,
               "result": {"class_name", "selector", "is_class_method",
                          "existed", "removed"}}.
    """
    return interop_remove_method(
        class_name, selector, is_class_method=is_class_method
    )


@mcp.tool("remove_class")
def remove_class(
    _: Context,
    class_name: Annotated[
        str, Field(description="Class name to remove from the image.")
    ],
) -> dict[str, Any]:
    """
    Remove a class from the image.

    Missing classes are reported as a successful no-op with
    `existed=false, removed=false`.

    Returns:
        dict: {"success": True,
               "result": {"class_name", "existed", "removed"}}.
    """
    return interop_remove_class(class_name)


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()
