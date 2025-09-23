import io
import os
import pytest
from block_parser import Parser


def test_success(tmp_path):
    content = """\
begin block b1
  item v1
  item v2
end block b1

begin block b2
  item v3
  # comment on v4
  item v4
  item v5
end block b2

# comment on b3, empty block
begin block b3
end block b3
"""
    p = Parser()
    fpath = tmp_path / "test_success.txt"
    fpath.write_text(content)
    blocks = p.parse(str(fpath))
    assert len(blocks) == 3, f'3 blocks expected, got {len(blocks)}'
    assert set(blocks.keys()) == set(('b1', 'b2', 'b3')), f'unexpected block names {set(blocks.keys())}'
    for i, nr_items in enumerate((2, 3, 0)):
        assert len(blocks[f'b{i + 1}']) == nr_items, 'expected {nr_items} for b{i + 1}'

CASES = [
    ("err_start_with_item.txt", "item v1", 'line 1: expecting begin block'),
    ("err_start_with_garbage.txt", "foo", 'line 1: expecting begin block'),
    ("err_unterminated_block.txt", "begin block b1\n  item v1\n", 'not ended at end of file'),
    ("err_mismatched_end.txt", "begin block b1\n  item v1\nend block b2\n", 'ended by "b2"'),
    ("err_stray_end_at_start.txt", "end block b1\n", 'line 1: expecting begin block'),
    ("err_nested_begin_inside_block.txt",
     "begin block b1\n  item v1\n  begin block inner\nend block b1\n",
     'expected item or end block'),
    ("err_garbage_inside_block.txt",
     "begin block b1\n  item v1\n  foo\nend block b1\n",
     'expected item or end block'),
    ("err_item_without_name.txt",
     "begin block b1\n  item\nend block b1\n",
     'expected item or end block'),
    ("err_end_with_trailing_garbage.txt",
     "begin block b1\n  item v1\nend block b1 extra\n",
     'expected item or end block'),
    ("err_illegal_block_name.txt", "begin block bad-name\n", 'expecting begin block'),
    ("err_item_outside_block.txt",
     "begin block b1\n  item v1\nend block b1\nitem vX\n",
     'expected begin block'),
]

@pytest.mark.parametrize("fname,content,needle", CASES)
def test_errors(tmp_path, fname, content, needle):
    p = Parser()
    fpath = tmp_path / fname
    fpath.write_text(content)
    with pytest.raises(ValueError) as e:
        p.parse(str(fpath))
    assert needle in str(e.value)
