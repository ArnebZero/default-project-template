import ast
import importlib
from pathlib import Path
from typing import Any, Callable, List, Optional, Type


def default_name_filter(name: str) -> bool:
    """Default name filter function that excludes private modules."""
    return not name.startswith("_")


def _check_target(
    node: ast.Assign | ast.AnnAssign,
    target: ast.expr,
    attribute_name: Optional[str] = None,
    attribute_value: Optional[Any] = None,
    check_attribute_value: bool = False,
) -> bool:
    if isinstance(target, ast.Name) and target.id == attribute_name:
        if not check_attribute_value or (
            isinstance(node.value, ast.Constant) and node.value.value == attribute_value
        ):
            return True
    return False


def _safe_check_file(
    file_path: Path,
    cls_name: str,
    attribute_name: Optional[str] = None,
    attribute_value: Optional[Any] = None,
    check_attribute_value: bool = False,
) -> bool:
    try:
        source = file_path.read_text()
        tree = ast.parse(source)
    except SyntaxError:
        return False

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == cls_name:
            if attribute_name is None:
                return True
            for body_node in node.body:
                if isinstance(body_node, ast.Assign):
                    for target in body_node.targets:
                        if _check_target(
                            node=body_node,
                            target=target,
                            attribute_name=attribute_name,
                            attribute_value=attribute_value,
                            check_attribute_value=check_attribute_value,
                        ):
                            return True

                elif isinstance(body_node, ast.AnnAssign):
                    if _check_target(
                        node=body_node,
                        target=body_node.target,
                        attribute_name=attribute_name,
                        attribute_value=attribute_value,
                        check_attribute_value=check_attribute_value,
                    ):
                        return True
    return False


def import_module(
    base: str,
    cls_name: str,
    attribute_name: Optional[str] = None,
    attribute_value: Optional[Any] = None,
    check_attribute_value: bool = False,
    file_path: Optional[Path | str] = None,
    package: Optional[str] = None,
    base_cls: Optional[Type[Any]] = None,
    name_filter: Optional[Callable] = None,
    safe: bool = True,
) -> List[Any]:
    """
    Import a class from modules within a base package.

    This function searches for modules within a specified base package and
    imports the modules containing a class with the specified name.

    Args:
        base: Base package path as a dot-separated string. If it starts with '.',
              it's treated as a relative import from file_path.
        cls_name: Name of the class to import from the modules.
        attribute_name: If not None, checks if the class has this attribute.
        file_path: Path to the file from which relative imports are resolved.
                   Required when base starts with '.'.
        package: Optional package name for the import. If provided, it is used
                 as the package argument in importlib.import_module.
        base_cls: Optional base class that the imported class must inherit from.
        name_filter: Optional function to filter module names. Defaults to
                    default_name_filter which excludes modules starting with '_'.
        safe: If True, uses AST to check if the class and attribute exist before importing.

    Returns:
        List of imported classes.
    """
    if base.startswith("."):
        if file_path is None:
            raise ValueError("'file_path' must be provided when base starts with '.'")
        base_path = Path(file_path)
        for part in base.split("."):
            if part == "":
                base_path = base_path.parent
            else:
                base_path = base_path / part
    else:
        module = importlib.import_module(base, package=package)
        base_path = Path(module.__file__).parent

    if name_filter is None:
        name_filter = default_name_filter

    modules = []
    for file in base_path.glob("*.py"):
        if not name_filter(file.stem):
            continue
        if safe and not _safe_check_file(
            file, cls_name, attribute_name, attribute_value, check_attribute_value
        ):
            continue
        module_name = file.stem
        try:
            if base.startswith("."):
                module = importlib.import_module(f"{base}.{module_name}", package=package)
            else:
                module = importlib.import_module(f"{base}.{module_name}")
        except ImportError as err:
            raise ImportError(f"Failed to import module '{file.stem}': {err}") from err
        cls = getattr(module, cls_name, None)
        if cls is None:
            continue
        if base_cls is not None and not issubclass(cls, base_cls):
            raise TypeError(
                f"Class '{cls_name}' in module '{module_name}' "
                f"is not a subclass of '{base_cls.__name__}'"
            )
        if attribute_name is not None:
            if not hasattr(cls, attribute_name):
                raise AttributeError(
                    f"Class '{cls_name}' in module '{module_name}' "
                    f"does not have attribute '{attribute_name}'"
                )
            if check_attribute_value:
                if not getattr(cls, attribute_name) == attribute_value:
                    raise ValueError(
                        f"Class '{cls_name}' in module '{module_name}' "
                        f"has attribute '{attribute_name}' but its value "
                        f"does not match the expected value"
                    )
        modules.append(cls)
    if len(modules) == 0:
        raise ImportError(f"No modules found in '{base}' with class '{cls_name}'")
    return modules
