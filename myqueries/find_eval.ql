import python

from Call c
where c.getFunc().(Name).getId() = "exec"
select c,
  c.getLocation().getFile().getRelativePath(),
  c.getLocation().getStartLine()
