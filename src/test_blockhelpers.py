import unittest

from blockhelpers import *

class TestBlockHelpers(unittest.TestCase):
    def testMarkdownBlock(self):
        text = ""
        text2 = "text"
        text3 = "     text    "
        text4 = "\n\n"
        text5 = "text\n\ntext"
        text6 = "text\ntext"
        text7 = "text\n\n\ntext"
        text8 = "text\n\n\n\ntext"
        self.assertEqual(markdown_to_blocks(text), [])
        self.assertEqual(markdown_to_blocks(text2), ["text"])
        self.assertEqual(markdown_to_blocks(text3), ["text"])
        self.assertEqual(markdown_to_blocks(text4), [])
        self.assertEqual(markdown_to_blocks(text5), ["text", "text"])
        self.assertEqual(markdown_to_blocks(text6), ["text\ntext"])
        self.assertEqual(markdown_to_blocks(text7), ["text", "text"])
        self.assertEqual(markdown_to_blocks(text8), ["text", "text"])
    
    def testBlockType(self):
        text = ""
        text2 = "paragraph"
        text3 = "#"
        header = "# header"
        header2 = "## header"
        header3 = "### header"
        header4 = "#### header"
        header5 = "##### header"
        header6 = "###### header"
        not_header = "####### paragraph"
        not_header2 = "#paragraph"
        code = "```code```"
        code2 = "```code\ncode```"
        not_code = "`not code`"
        not_code2 = "``not code``"
        not_code3 = "```not code"
        not_code4 = "`not code```"
        quote = ">quote"
        quote2 = "> quote"
        quote3 = "> quote\n>quote"
        not_quote = "> not quote\nnot quote"
        unordered = "* unordered"
        unordered2 = "- unordered"
        unordered3 = "* unordered\n* unordered"
        unordered4 = "- unordered\n- unordered"
        unordered5 = "* unordered\n- unordered"
        not_unordered = "*not unordered"
        not_unordered2 = "-not unordered"
        not_unordered3 = "* not unordered\n*not unordered"
        not_unordered4 = "* not unordered\nnot unordered"
        ordered = "1. ordered"
        ordered2 = "1. ordered\n2. ordered"
        ordered3 = "1. ordered\n2. ordered\n3. ordered\n4. ordered\n5. ordered\n6. ordered\n7. ordered\n8. ordered\n9. ordered\n10. ordered"
        not_ordered = "1.not ordered"
        not_ordered2 = "1 not ordered"
        not_ordered3 = "1. not ordered\n2.not ordered"
        not_ordered4 = "1. not ordered\n3. not ordered"
        not_ordered5 = "1. not ordered\nnot ordered"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(text3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(header), BlockType.HEADING)
        self.assertEqual(block_to_block_type(header2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(header3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(header4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(header5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(header6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(not_header), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_header2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        self.assertEqual(block_to_block_type(code2), BlockType.CODE)
        self.assertEqual(block_to_block_type(not_code), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_code2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_code3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_code4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote3), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(not_quote), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(unordered), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type(unordered2), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type(unordered3), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type(unordered4), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type(unordered5), BlockType.UNORDERED)
        self.assertEqual(block_to_block_type(not_unordered), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_unordered2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_unordered3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_unordered4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(ordered), BlockType.ORDERED)
        self.assertEqual(block_to_block_type(ordered2), BlockType.ORDERED)
        self.assertEqual(block_to_block_type(ordered3), BlockType.ORDERED)
        self.assertEqual(block_to_block_type(not_ordered), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ordered2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ordered3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ordered4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_ordered5), BlockType.PARAGRAPH)
    
    def testExtractHeaders(self):
        text = "# title"
        text2 = "## not title\n\n# title"
        text3 = "# title\n\nnot title"
        text4 = "# title\n\n# also h1 but not title"
        self.assertEqual(extract_title(text), "title")
        self.assertEqual(extract_title(text2), "title")
        self.assertEqual(extract_title(text3), "title")
        self.assertEqual(extract_title(text4), "title")
    
    def testExtractErr(self):
        text = "this should error"
        self.assertRaises(Exception, extract_title, text)



if __name__ == "__main__":
    unittest.main()