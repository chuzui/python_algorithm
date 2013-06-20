public class RatioIndex implements Comparable<RatioIndex>{
    public double Ratio;
    public int Index;

    public RatioIndex(double ratio, int index){
        this.Ratio = ratio;
        this.Index = index;

    }

    public int compareTo(RatioIndex that) {
        if (this.Ratio < that.Ratio)
            return 1;

        if (this.Ratio > that.Ratio)
            return -1;
        return 0;
    }
}