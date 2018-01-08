package edu.cmu.ml.rtw.pra.features;

/**
 * Created by shell on 10/14/16.
 */
public class SparseMatrixRow {
    final public int[] featureTypes;
    final public double[] values;
    public SparseMatrixRow(int[] featureTypes, double[] values){
        this.featureTypes=featureTypes;
        this.values=values;
    }

}

