package eu.su.mas.dedaleEtu.mas.behaviours.knowledge;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import dataStructures.tuple.Couple;
import eu.su.mas.dedale.env.Observation;
import eu.su.mas.dedale.mas.AbstractDedaleAgent;
import eu.su.mas.dedaleEtu.mas.agents.dummies.ExploreSoloAgent;
import eu.su.mas.dedaleEtu.mas.knowledge.MapRepresentation;
import eu.su.mas.dedaleEtu.mas.knowledge.MapRepresentation.MapAttribute;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.SimpleBehaviour;


/**
 * This behaviour allows an agent to explore the environment and learn the associated topological map.
 * The algorithm is a pseudo - DFS computationally consuming because its not optimised at all.</br>
 * 
 * When all the nodes around him are visited, the agent randomly select an open node and go there to restart its dfs.</br> 
 * This (non optimal) behaviour is done until all nodes are explored. </br> 
 * 
 * Warning, this behaviour does not save the content of visited nodes, only the topology.</br> 
 * Warning, this behaviour is a solo exploration and does not take into account the presence of other agents (or well) and indefinitely tries to reach its target node
 * @author hc
 *
 */
public class MappingBehaviour extends SimpleBehaviour {

	private static final long serialVersionUID = 8567689731496787661L;

	private boolean finished = false;

	/**
	 * Current knowledge of the agent regarding the environment
	 */
	private MapRepresentation myMap;

	/**
	 * Nodes known but not yet visited
	 */
	private List<String> openNodes;
	/**
	 * Visited nodes
	 */
	private Set<String> closedNodes;
	
	private String nextNode = null;


	public MappingBehaviour(final AbstractDedaleAgent myagent) {
		super(myagent);
		this.openNodes=new ArrayList<String>();
		this.closedNodes=new HashSet<String>();
	}
	
	public void mergeMap(List<String> openNodes,Set<String> closedNodes,List<String> edges) {

		for (String n : closedNodes) {
			if(!this.closedNodes.contains(n)) {
				this.myMap.addNode(n,MapAttribute.closed);
				this.closedNodes.add(n);
			}
        }
		for (String n : openNodes) {
			if(!this.openNodes.contains(n)) {
				this.myMap.addNode(n,MapAttribute.open);
				this.openNodes.add(n);
			}
        }
		
		List<String> myEdges = myMap.getEdges();
		
		for (String e : edges) {
			if(!myEdges.contains(e)) {
				String [] s = e.split(",");
				String e0 = s[0];
				String e1 = s[1];
				boolean b0 = closedNodes.contains(e0) || openNodes.contains(e0);
				boolean b1 = closedNodes.contains(e1) || openNodes.contains(e1);
				if(b0 && b1) {
					this.myMap.addEdge(e0, e1);
				}
			}
		}
	
		this.openNodes.removeAll(closedNodes);
		
	}

	@Override
	public void action() {

		if(this.myMap==null)
			this.myMap= new MapRepresentation();
		
		//0) Retrieve the current position
		String myPosition=((AbstractDedaleAgent)this.myAgent).getCurrentPosition();
	
		if (myPosition!=null){
			//List of observable from the agent's current position
			List<Couple<String,List<Couple<Observation,Integer>>>> lobs=((AbstractDedaleAgent)this.myAgent).observe();//myPosition

			/**
			 * Just added here to let you see what the agent is doing, otherwise he will be too quick
			 */
			try {
				this.myAgent.doWait(500);
			} catch (Exception e) {
				e.printStackTrace();
			}

			//1) remove the current node from openlist and add it to closedNodes.
			this.closedNodes.add(myPosition);
			this.openNodes.remove(myPosition);

			this.myMap.addNode(myPosition,MapAttribute.closed);

			//2) get the surrounding nodes and, if not in closedNodes, add them to open nodes.
			this.nextNode=null;
			Iterator<Couple<String, List<Couple<Observation, Integer>>>> iter=lobs.iterator();
			while(iter.hasNext()){
				String nodeId=iter.next().getLeft();
				if (!this.closedNodes.contains(nodeId)){
					if (!this.openNodes.contains(nodeId)){
						this.openNodes.add(nodeId);
						this.myMap.addNode(nodeId, MapAttribute.open);
						this.myMap.addEdge(myPosition, nodeId);	
					}else{
						//the node exist, but not necessarily the edge
						this.myMap.addEdge(myPosition, nodeId);
					}
					if (nextNode==null) nextNode=nodeId;
				}
			}
				
			}

		}

	@Override
	public boolean done() {
		return finished;
	}
	
	public String getNextNode(String position) {
		
		if(this.nextNode!=null) return this.nextNode;
		
		if(this.openNodes.isEmpty()) return "";
		
		return this.myMap.getShortestPath(position, this.openNodes.get(0)).get(0);
	}

	public List<String> getOpenNodes() {
		return openNodes;
	}

	public Set<String> getClosedNodes() {
		return closedNodes;
	}
	
	public List<String> getEdges() {
		return myMap.getEdges();
	}
	
	public MapRepresentation getMyMap() {
		if(this.myMap==null)
			this.myMap= new MapRepresentation();
		return myMap;
	}
}
