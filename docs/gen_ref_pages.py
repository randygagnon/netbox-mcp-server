"""Generate the code reference pages."""

from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

# Document main modules
for path in sorted(Path("").glob("*.py")):
    module_path = path.relative_to("").with_suffix("")
    doc_path = path.relative_to("").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    nav[module_path.parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(module_path.parts)
        fd.write(f"::: {identifier}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Generate navigation
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav()) 