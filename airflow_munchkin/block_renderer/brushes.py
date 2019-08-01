# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.block_generator.blocks import (
    CodeBlock,
    MethodBlock,
    ClassBlock,
    FileBlock,
)
from airflow_munchkin.block_renderer.template_utils import render_template


def render_code_block(code_block: CodeBlock) -> str:
    logging.info("Rendering code block: %s", code_block.template_name)

    return render_template(
        template_name=f"code_blocks/{code_block.template_name}",
        **code_block.template_params,
    )


def render_method_block(method_block: MethodBlock) -> str:
    logging.info("Rendering method block: %s", method_block.name)

    code_blocks = [render_code_block(block) for block in method_block.code_blocks]
    decorator_blocks = [
        render_code_block(block) for block in method_block.decorator_blocks
    ]

    return render_template(
        template_name="method_block.py.tpl",
        name=method_block.name,
        desc=method_block.desc if method_block.name != "__init__" else None,
        args=method_block.args,
        return_kind=method_block.return_kind,
        return_desc=method_block.return_desc,
        code_blocks=code_blocks,
        decorator_blocks=decorator_blocks,
    )


def render_class_block(class_block: ClassBlock) -> str:
    logging.info("Rendering class block: %s", class_block.name)

    method_blocks = [render_method_block(block) for block in class_block.methods_blocks]

    ctor_method_block = next(
        (block for block in class_block.methods_blocks if block.name == "__init__"),
        None,
    )

    return render_template(
        template_name="class_block.py.tpl",
        name=class_block.name,
        extend_class=class_block.extend_class,
        ctor_method=ctor_method_block,
        method_blocks=method_blocks,
    )


def render_file_block(file_block: FileBlock) -> str:
    logging.info("Rendering file block: %s", file_block.file_name)

    class_blocks = [render_class_block(block) for block in file_block.class_blocks]

    return render_template(
        template_name="file_block.py.tpl",
        class_blocks=class_blocks,
        import_statement=file_block.import_statement,
        constants=file_block.constants,
    )
