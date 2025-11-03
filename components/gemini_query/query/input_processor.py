#!/usr/bin/env python3
"""
Input processing for Gemini Auto Query.

This module handles command line argument processing and stdin reading
with proper error handling and encoding support.
"""

import logging
import sys


class InputProcessor:
    """Input processor for command line arguments and stdin"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_input_data(self, args: list[str]) -> str:
        """
        Extract input data from command line arguments and stdin.

        Args:
            args: Command line arguments

        Returns:
            Combined input string from arguments and stdin
        """
        # Extract command line arguments (skip script name)
        question = self._get_args_input(args)

        # Read piped input if available
        piped_input = self._get_stdin_input()

        # Combine inputs with proper formatting
        return self._combine_inputs(question, piped_input)

    def _get_args_input(self, args: list[str]) -> str:
        """Extract input from command line arguments"""
        return ' '.join(args[1:]) if len(args) > 1 else ''

    def _get_stdin_input(self) -> str:
        """Read input from stdin if available"""
        if sys.stdin.isatty():
            return ''

        try:
            piped_input = sys.stdin.read().strip()
            self.logger.debug(f"Read {len(piped_input)} characters from stdin")
            return piped_input
        except OSError as error:
            self.logger.warning(f"Could not read from stdin: {error}")
            return ''

    def _combine_inputs(self, question: str, piped_input: str) -> str:
        """Combine question and piped input with proper formatting"""
        if question and piped_input:
            combined = f"{question}\n\n{piped_input}"
        elif question:
            combined = question
        elif piped_input:
            combined = piped_input
        else:
            combined = ''

        return combined.strip()
