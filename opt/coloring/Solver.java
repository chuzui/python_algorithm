import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

/**
 * Created with IntelliJ IDEA.
 * User: Administrator
 * Date: 13-6-25
 * Time: ÏÂÎç9:28
 * To change this template use File | Settings | File Templates.
 */
public class Solver {

    public static void main(String[] args) {
        try {
            solve(args);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public final void colorSpace(int node, int nodeColor, int[][] edges){

    }

    public static void solve(String[] args) throws IOException {
        String fileName = null;

        // get the temp file name
        for(String arg : args){
            if(arg.startsWith("-file=")){
                fileName = arg.substring(6);
            }
        }
        if(fileName == null)
            return;

        // read the lines out of the file
        List<String> lines = new ArrayList<String>();

        BufferedReader input =  new BufferedReader(new FileReader(fileName));
        try {
            String line = null;
            while (( line = input.readLine()) != null){
                lines.add(line);
            }
        }
        finally {
            input.close();
        }


        // parse the data in the file
        String[] firstLine = lines.get(0).split("\\s+");
        int nodeCount = Integer.parseInt(firstLine[0]);
        int edgeCount = Integer.parseInt(firstLine[1]);

        int[][] edges = new int[nodeCount][nodeCount];
        int v, w;
        for (int i = 1; i < edgeCount + 1; i++){
            String line = lines.get(i);
            String[] parts = line.split("\\s+");
            v = Integer.parseInt(parts[0]);
            w = Integer.parseInt(parts[1]);
            edges[v][w] = 1;
            edges[w][v] = 1;


        }

        Stack<State> s = new Stack<State>();
        s.push(new State(1, 0, 0));

        int minColorsNum = nodeCount + 1;
        int[] minNodesColor = new int[nodeCount];
        int[] nodesColor = new int[nodeCount];
        int node, color, colorCount, newNode;
        int end = nodeCount - 1;
        boolean flag;
        while (!s.empty()){
            State state = s.pop();
            node = state.Node;
            if (state.ColorCount < minColorsNum){
                color = state.NodeColor;
                nodesColor[node] = color;
                if (node == end){
                    minColorsNum = state.ColorCount;
                    minNodesColor = nodesColor.clone();
                }
                else{
                    colorCount = state.ColorCount;
                    newNode = node + 1;
                    s.push(new State(colorCount + 1, newNode, colorCount));
                    for (int i= 0; i < colorCount; i++){
                         flag = true;
                         for (int j = 0; j <= node; j++){
                              if (edges[newNode][j] == 1 && nodesColor[j] == i){
                                  flag = false;
                                  break;
                              }
                         }

                        if (flag){
                            s.push(new State(colorCount, newNode, i));
                        }
                    }
                }
            }
        }
	minColorsNum -= 1;
        System.out.println(minColorsNum+" 1");
        for(int i=0; i < nodeCount; i++){
            System.out.print(minNodesColor[i]+" ");
        }
        System.out.println("");
    }
}
