/**
 * @name Propagation des entrees non fiables
 * @kind path-problem
 * @id py/taint-spread
 * @problem.severity recommendation
 */
import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources

module SpreadConfig implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) { source instanceof RemoteFlowSource }
  predicate isSink(DataFlow::Node sink) {
    exists(DataFlow::CallCfgNode call | sink = call.getArg(_))
  }
}
module Spread = TaintTracking::Global<SpreadConfig>;
import Spread::PathGraph

from Spread::PathNode source, Spread::PathNode sink
where Spread::flowPath(source, sink)
select sink.getNode(), source, sink, "Entree non fiable qui se propage jusqu'ici."
