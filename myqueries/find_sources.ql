import python
import semmle.python.dataflow.new.RemoteFlowSources

from RemoteFlowSource source
select
  source.getLocation().getFile().getRelativePath() as fichier,
  source.getLocation().getStartLine() as ligne,
  source.getScope().getName() as fonction,
  source.getSourceType() as type
