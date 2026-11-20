/**
 * @name Untrusted input to eval
 * @kind path-problem
 * @id py/eocon-taint-to-eval
 * @problem.severity error
 */
import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources
import semmle.python.ApiGraphs

module EvalConfig implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node source) { source instanceof RemoteFlowSource }
  predicate isSink(DataFlow::Node sink) {
    sink = API::builtin("eval").getACall().getArg(0)
  }
}
module EvalFlow = TaintTracking::Global<EvalConfig>;
import EvalFlow::PathGraph

from EvalFlow::PathNode source, EvalFlow::PathNode sink
where EvalFlow::flowPath(source, sink)
select sink.getNode(), source, sink, "Entree non fiable atteignant eval."
