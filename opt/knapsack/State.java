/**
 * Created with IntelliJ IDEA.
 * User: Administrator
 * Date: 13-6-20
 * Time: 下午8:36
 * To change this template use File | Settings | File Templates.
 */
public class State {
    public int index;
    public int value;
    public int weight;
    public double estimate;
    public int isSelected;

    public State(int i, int v, int w, double e, int isS){
        index = i;
        value = v;
        weight = w;
        estimate = e;
        isSelected = isS;
    }
}
