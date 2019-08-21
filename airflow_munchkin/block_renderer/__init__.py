# -*- coding: utf-8 -*-
import logging
from os import path
from typing import List


from airflow_munchkin.block_generator.blocks import FileBlock
from airflow_munchkin.block_renderer import cosmetics, brushes
from airflow_munchkin.config import OUTPUT_PATH


def create_file_from_file_block(file_block: FileBlock) -> None:
    logging.info("Creating file: %ss", file_block.file_name)
    output_file_name = path.join(OUTPUT_PATH, file_block.file_name)

    with open(output_file_name, "w") as file:
        file_content = brushes.render_file_block(file_block)
        file.write(file_content)

    cosmetics.format_with_black(output_file_name)
    cosmetics.sort_imports(output_file_name)
    cosmetics.remove_unused_imports(output_file_name)


def create_files_from_file_blocks(file_blocks: List[FileBlock]) -> None:
    logging.info("Start rendering blocks")
    for file_block in file_blocks:
        create_file_from_file_block(file_block=file_block)
    logging.info("Finished rendering blocks")
