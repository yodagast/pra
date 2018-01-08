package edu.cmu.ml.rtw.pra.data

import edu.cmu.ml.rtw.pra.graphs.Graph

sealed abstract class Instance(val isPositive: Boolean, val graph: Graph) {
  def stringKey(): String

  // Sometimes we get instances that are not in the graph, for various reasons.  This lets us catch
  // those and return empty feature vectors without needing to make the graph search code check for
  // invalid input.
  def isInGraph(): Boolean
  def getString(): String
}

class NodeInstance(
  val node: Int,
  isPositive: Boolean,
  graph: Graph
) extends Instance(isPositive, graph) {
  override def stringKey() = "" + node
  override def isInGraph() = node >= 0
  override def toString() = {
    val pos = if (isPositive) 1 else -1
    s"${graph.getNodeName(node)}\t$pos"
  }
  def getString():String = {
    val pos = if (isPositive) 1 else -1
    return node.toString()+"\t"+pos.toString
  }
}

class NodePairInstance(
  val source: Int,
  val target: Int,
  isPositive: Boolean,
  graph: Graph
) extends Instance(isPositive, graph) {
  override def stringKey() = source + " " + target
  override def isInGraph() = source >= 0 && target >= 0
  override def toString() = {
    val pos = if (isPositive) 1 else -1
    s"${graph.getNodeName(source)}\t${graph.getNodeName(target)}\t$pos"
  }
  def getString():String = {
    val pos = if (isPositive) 1 else -1
    var s1=graph.getNodeName(source)
    var s2=graph.getNodeName(target)
    return s1+"\t"+s2+"\t"+"\t"+pos.toString
  }
}

