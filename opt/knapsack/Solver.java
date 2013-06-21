import java.io.*;
import java.lang.ArrayStoreException;
import java.lang.Comparable;
import java.lang.System;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Stack;

/**
 * The class <code>Solver</code> is an implementation of a greedy algorithm to solve the knapsack problem.
 *
 */
public class Solver {
    
    /**
     * The main class
     */
    public static void main(String[] args) {
        try {
            solve(args);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Read the instance, solve it, and print the solution in the standard output
     */
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
        int items = Integer.parseInt(firstLine[0]);
        int capacity = Integer.parseInt(firstLine[1]);

        int[] values = new int[items];
        int[] weights = new int[items];

        for(int i=1; i < items+1; i++){
          String line = lines.get(i);
          String[] parts = line.split("\\s+");

          values[i-1] = Integer.parseInt(parts[0]);
          weights[i-1] = Integer.parseInt(parts[1]);
        }

        // a trivial greedy algorithm for filling the knapsack
        // it takes items in-order until the knapsack is full
        int value = 0;
        int weight = 0;
        int[] taken = new int[items];

//        for(int i=0; i < items; i++){
//            if(weight + weights[i] <= capacity){
//                taken[i] = 1;
//                value += values[i];
//                weight += weights[i];
//            } else {
//                taken[i] = 0;
//            }
//        }0

        value = depth(capacity, weights, values, taken);


        // prepare the solution in the specified output format
        System.out.println(value+" 1");
        for(int i=0; i < items; i++){
            System.out.print(taken[i]+" ");
        }
        System.out.println("");        
    }

    private static int depth(int k, int[] weights, int[] values, int[] takens){
        int l = weights.length;
        RatioIndex[] ratios = new RatioIndex[l];
        for (int i = 0; i < l; i++){
            double ratio = (double)values[i] / weights[i];
            ratios[i] = new RatioIndex(ratio, i);
        }
        Arrays.sort(ratios);
//        for(int i = 0; i < l; i++){
//            System.out.printf("%f ", ratios[i].Ratio);
//        }
        Stack<State> s = new Stack<State>();

        int index = ratios[0].Index;
        s.push(new State(0, 0, k, estimate(ratios, k, 1, weights, values), 0));
        s.push(new State(0, values[index], k-weights[index], values[index] + estimate(ratios, k-weights[index], 1, weights, values), 1));

        int maxV = 0;

        int[] maxToken = new int[l];

        int end = l - 1;
        while (!s.empty()){
            State state = s.pop();
            takens[state.index] = state.isSelected;
            //if (state.weight >= 0){
                index = state.index;
                if (index == end){
                    if (state.value > maxV){
                        maxV = state.value;
                        maxToken = takens.clone();
                    }
                }
                else{
                    //if (state.estimate > maxV){
                        int newIndex = ratios[index+1].Index;
                        int nextIndex = index + 1;
                        double e = state.value + estimate(ratios, state.weight, nextIndex, weights, values);
                        if (e > maxV){
                            s.push(new State(nextIndex, state.value, state.weight, e, 0));
                        }
                        int w = state.weight - weights[newIndex];
                        if (w > 0)
                        {
                            s.push(new State(nextIndex, state.value + values[newIndex], w,
                                    state.estimate, 1));
                        }
                    //}
                }
            //}
        }

//        for (int i = 0; i < l; i++){
//           System.out.printf("%d ", maxToken[i] );
//        }
        for (int i = 0; i < l; i++){
            takens[ratios[i].Index] = maxToken[i];
        }
        return maxV;
    }

    private static double estimate(RatioIndex[] ratios, int k, int start, int[] weights, int[] values){
        int l = ratios.length;
        int tempK = k;
        double e = 0;

        for (int i = start; i < l; i++){
            int index = ratios[i].Index;
            if (tempK > weights[index]){
                e += values[index];
                tempK -= weights[index];
            }
            else{
                e += values[index] * ((double)tempK / weights[index]);
                break;
            }
        }
        return e;
    }
}