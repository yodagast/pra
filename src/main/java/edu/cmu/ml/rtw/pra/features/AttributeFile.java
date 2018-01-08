package edu.cmu.ml.rtw.pra.features;

import cc.mallet.types.Alphabet;
import cc.mallet.types.FeatureVector;
import edu.cmu.ml.rtw.pra.data.Instance;

import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.regex.Pattern;

/**
 * Created by shell on 9/6/16.
 */

public class AttributeFile {
    public static final String baseDir="/home/kdeapp/KBCompletion/Data/matrix_sfe/";
    public static final String baseDir1="/home/kdeapp/KBCompletion/Data/";
    public static void makeDir(String s){
        File f=new File(s);
        if(!f.exists() ){
            f.mkdir();
        }
    }

    public  List<String> loadLiteralDict(String fileName) throws  IOException{
        FileReader fileReader=new FileReader(baseDir1+fileName);
        BufferedReader dict=new BufferedReader(fileReader);
        String str="";
        List<String> arrayList=new ArrayList<>();
        while ((str=dict.readLine())!=null){
            arrayList.add(str);
        }
        return arrayList;
    }
    public  List<String> loadLiteralDict(String fileName,String tmp) throws  IOException{
        FileReader fileReader=new FileReader(baseDir1+fileName);
        BufferedReader dict=new BufferedReader(fileReader);
        String str="";
        List<String> arrayList=new ArrayList<>();
        while ((str=dict.readLine())!=null){
            arrayList.add(str+tmp);
        }
        return arrayList;
    }

    public  ArrayList<SparseMatrixRow> loadDense2SparseMatrix(String relation,boolean isTraining,int max) throws  IOException{
        if(isTraining) {
            ArrayList<ArrayList<Double>> arrayLists= loadDenseMatrixRows(baseDir + relation + "/trainLiteralMatrix.csv");
            arrayLists=addFeatureInDenseMatrix(arrayLists);
            return convertDnese2SparseMatrix(arrayLists,max);
        }
        else {
            ArrayList<ArrayList<Double>> arrayLists= loadDenseMatrixRows(baseDir + relation + "/testLiteralMatrix.csv");
            arrayLists=addFeatureInDenseMatrix(arrayLists);
            return convertDnese2SparseMatrix(arrayLists,max);
        }
    }

    public ArrayList<ArrayList<Double>> loadDenseMatrix(String relation,boolean isTraining,int max) throws IOException{
        //AttributeFile attributeFile=new AttributeFile();
        if(isTraining) {
            ArrayList<ArrayList<Double>> arrayLists=loadDenseMatrixRows(baseDir + relation + "/trainLiteralMatrix.csv");
            arrayLists=addFeatureInDenseMatrix(arrayLists);
            return arrayLists;
        }
        else {
            ArrayList<ArrayList<Double>> arrayLists= loadDenseMatrixRows(baseDir + relation + "/testLiteralMatrix.csv");
            arrayLists=addFeatureInDenseMatrix(arrayLists);
            return arrayLists;
        }
    }

    public  ArrayList<ArrayList<Double>>  loadDenseMatrixRows(String fileName) throws IOException{
        String decimalPattern = "([0-9]*)\\.([0-9]*)";
        FileReader literalFile =new FileReader(fileName);
        BufferedReader literalBR=new BufferedReader(literalFile);
        String string="";
        ArrayList<ArrayList<Double>> arrayLists=new ArrayList<>();
        while ((string=literalBR.readLine())!=null){
            String[] str=string.split("\t");
            ArrayList<Double> arrayList=new ArrayList<>();
            for(int i=0;i<str.length;i++) {
                if (Pattern.matches(decimalPattern, str[i]))
                    arrayList.add( Double.parseDouble(str[i]));
                else arrayList.add(1.0);
            }
            arrayLists.add(arrayList);
        }
        return arrayLists;
    }
   //max 保存relation中最大的indice number
    public ArrayList<SparseMatrixRow> convertDnese2SparseMatrix(ArrayList<ArrayList<Double>> arrayLists,int max){
        ArrayList<SparseMatrixRow> sparseMatrixRows=new ArrayList<>();
        for(int i=0;i<arrayLists.size();i++ ){
            ArrayList<Double> arrayList=arrayLists.get(i);
            int[] indice=new int[arrayList.size()];
            double[] value=new double[arrayList.size()];
            for(int j=0;j<arrayList.size();j++){
                if(Math.abs(arrayList.get(j)-0)>0.01 ){
                    indice[j]=j+max;
                    value[j]=arrayList.get(j);
                }
            }
            SparseMatrixRow sparseMatrixRow=new SparseMatrixRow(indice,value);
            sparseMatrixRows.add(sparseMatrixRow);
        }
        return sparseMatrixRows;
    }

    //TODO 增加densematrix中的特征
    //TODO maxmin 处理矩阵
    //前六列日期数据 处理,计算差值

    public  ArrayList<ArrayList<Double>> addFeatureInDenseMatrix(ArrayList<ArrayList<Double>> arrayLists){
        if(arrayLists.size()<1) return null;
        int columns=arrayLists.get(0).size();
        int row=arrayLists.size();
        double[][] raw=new double[row][columns];
        for(int i=0;i<row;i++)
            for(int j=0;j<columns;j++)
                raw[i][j]=arrayLists.get(i).get(j);

        double[][] ans=new double[row][columns+6];
        for(int i=0;i<row;i++)
            for(int j=0;j<columns;j++)
                ans[i][j]=arrayLists.get(i).get(j);
        //计算前六列日期差值
        for(int i=0;i<row;i++){
            int half=columns/2;
            for(int j=0;j<6;j++){
                if(raw[i][j]>1000 &&raw[i][j+half]>1000)
                    ans[i][j+columns]=dateSubtraction(raw[i][j],raw[i][j+half]);
            }
        }
        //第八列以后进行maxmin处理
        ans=maxMinMatrix(ans);
        return convertMatrix2ArrayList(ans);
    }
    //maxmin处理matrix
    //从第1-8列\36-43列需要设0
    public  double[][] maxMinMatrix(double[][] matrix){
        int row=matrix.length;
        if(row<1) return null;
        int col=matrix[0].length;
        for(int j=0;j<col;j++){
            //if(j>=35 && j<=42) continue;
            if(matrix[0][j]>1000){
                for(int i=0;i<row;i++) {
                    if (matrix[i][j] > 0 || matrix[i][j] < 0)
                        matrix[i][j] = 1.0;
                    else matrix[i][j] = 0;
                }
            }else {
                double[] tmp = new double[row];
                for (int i = 0; i < row; i++)
                    tmp[i] = matrix[i][j];
                double max = maxNum(tmp);
                double min = minNum(tmp);
                for (int i = 0; i < row; i++)
                    if (max > min && max > 0)
                        matrix[i][j] = (matrix[i][j] - min) / (max - min);
            }
        }
        return matrix;
    }
    public  double maxNum(double[] array){
        if(array.length<1) return 0;
        double max=array[0];
        for(int i=1;i<array.length;i++)
            max=Math.max(max,array[i]);
        return max;
    }
    public double minNum(double[] array){
        if(array.length<1) return 0;
        double min=array[0];
        for (int i=1;i<array.length;i++)
            min=Math.min(min,array[i]);
        return min;
    }
    //TODO 计算日期差值
    public double dateSubtraction(double d1,double d2) {
        SimpleDateFormat ft = new SimpleDateFormat ("yyyy.MMdd");
        Date t1=null;
        Date t2=null;
        try {
            String s1=Double.toString(d1);
            String s2=Double.toString(d2);
            if(s1.length()<9) {
                int tmp=9-s1.length();
                StringBuffer stringBuffer=new StringBuffer();
                for(int i=0;i<tmp;i++)
                    stringBuffer.append("0");
                s1=s1+stringBuffer.toString();
            }

            if(s2.length()<9) {
                int tmp=9-s2.length();
                StringBuffer stringBuffer=new StringBuffer();
                for(int i=0;i<tmp;i++)
                    stringBuffer.append("0");
                s2=s2+stringBuffer.toString();
            }
            t1=ft.parse(s1);
            t2=ft.parse(s2);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return (t2.getTime()-t1.getTime())/ 1000 / 60 / 60 / 24;
    }
    public ArrayList<ArrayList<Double>> convertMatrix2ArrayList(double[][] matrix){
        int row =matrix.length;
        if(row<1) return null;
        int col=matrix[0].length;
        ArrayList<ArrayList<Double>> arrayLists=new ArrayList<>();
        for(int i=0;i<row;i++){
            ArrayList<Double> arrayList=new ArrayList<>();
            for(int j=0;j<col;j++)
               if(matrix[i][j]>1.0) arrayList.add(1.0);
               else if(matrix[i][j]<0) arrayList.add(-1.0);
            arrayLists.add(arrayList);
        }
        return arrayLists;

    }



//读取sparseliteral矩阵
    public ArrayList<SparseMatrixRow>  loadSparseMatrix(String relation,boolean isTraining,int max) throws IOException{
        if(isTraining)
            return loadSparseMatrixRows(baseDir+relation+"/trainSparseLiteralMatrix.csv",max);
        else
            return loadSparseMatrixRows(baseDir+relation+"/testSparseLiteralMatrix.csv",max);
    }


    public FeatureMatrix mergeMatrix(ArrayList<SparseMatrixRow> sparseMatrixRows, FeatureMatrix featureMatrix){
        ArrayList<MatrixRow> arrayList=new ArrayList<>();
        System.out.println(featureMatrix.size()+"\t"+sparseMatrixRows.size());
        for(int i=0;i<featureMatrix.size();i++){
            SparseMatrixRow sparseMatrixRow;
            if(i>=sparseMatrixRows.size())
                sparseMatrixRow=new SparseMatrixRow(new int[1],new double[1]);
            else sparseMatrixRow=sparseMatrixRows.get(i);
            int[] indice=sparseMatrixRow.featureTypes;
            double[] value=sparseMatrixRow.values;

            MatrixRow mr = featureMatrix.getRow(i);
            int[] indice1=mr.featureTypes;
            double[] value1=mr.values;

            int len=Math.min(indice.length+indice1.length,value.length+value1.length);

            int[] idx=new int[len];
            double[] v=new double[len];
            System.arraycopy(indice1,0,idx,0,indice1.length);
            System.arraycopy(indice,0,idx,indice1.length,len-indice1.length);
            System.arraycopy(value1,0,v,0,value1.length);
            System.arraycopy(value,0,v,value1.length,len-value1.length);
            MatrixRow mr1=new MatrixRow(mr.instance,idx,v);
            arrayList.add(mr1);
        }
        return new FeatureMatrix(arrayList);
    }
    //解析head-tail 三元组和三元组中的literalfacts
    //在literal-fact中添加新的属性

    public  ArrayList<SparseMatrixRow> loadSparseMatrixRows(String fileName,int max) throws IOException{
        String str="";
        ArrayList<SparseMatrixRow> sparseMatrixRows=new ArrayList<>();

        FileReader literalFile =new FileReader(fileName);
        BufferedReader literalBR=new BufferedReader(literalFile);
        String decimalPattern = "([0-9]*)\\.([0-9]*)";
        while ((str=literalBR.readLine())!=null){
            String[] strings=str.split(";");
            if(strings.length!=2) continue;
            String[] str1=strings[0].split("\t");
            String[] str2=strings[1].split("\t");

            int [] indice=new int[1];
            double[] values=new double[1];
            if(str1.length>1 &&(str1.length)==str2.length){
                values=new double[str2.length];
                indice=new int[str1.length];
            }
            for(int i=0;i<str1.length;i++)
                indice[i]=Integer.parseInt(str1[i])+max;

            for(int i=0;i<str2.length;i++){
                if(Pattern.matches(decimalPattern,str2[i]))
                     values[i]=Double.parseDouble(str2[i]);
                if(values[i]>0) values[i]=1.0;
                else if(values[i]<0) values[i]=-1.0;
            }
            SparseMatrixRow sparseMatrixRow=new SparseMatrixRow(indice,values);
            sparseMatrixRows.add(sparseMatrixRow);
        }
        return sparseMatrixRows;
    }

    public static void writelibsvm(String relation, String trainOrTest,String[] featureTypes,FeatureMatrix featureMatrix) throws IOException {
        String dir=baseDir+relation;
        //makeDir(dir);
        FileWriter fw=new FileWriter(new File(dir+"/"+trainOrTest));
        int n=featureMatrix.size();
        int max=-1;

        //获得矩阵列数
        for(int i=0;i<n;i++)
            max=Math.max(max,featureMatrix.getRow(i).values.length);

        Alphabet alphabet= new Alphabet(featureTypes);
        //写入矩阵数据
        for(int i=0;i<n;i++){
            MatrixRow mr=featureMatrix.getRow(i);
            FeatureVector feature_vector = new FeatureVector(alphabet, mr.featureTypes, mr.values);
            if(mr.instance.isPositive()) {
                fw.write(mr.instance.toString()+"\t1 ");
            } else {
               // fw.write(i+"\t"+n+"\t"+featureTypes.length + "\t" + 0.0 + ";");
                fw.write(mr.instance.toString()+"\t-1 ");
            }
            double[] num=feature_vector.getValues();
            //System.out.println("********************featureTypes has length :"+featureTypes.length);
            //System.out.println("********************feature vector has length :"+num.length);
            int[] indice=feature_vector.getIndices();
            for(int k=0;k<indice.length;k++){
                fw.write(indice[k]+":"+num[k]+" ");
            }
            fw.write("\n");
        }
        fw.flush();
        fw.close();
    }

    public static void writePathTypes(String relation, String trainOrTest,String[] featureTypes,FeatureMatrix featureMatrix) throws IOException {
        String dir=baseDir+relation;
        //makeDir(dir);
        FileWriter fw=new FileWriter(new File(dir+"/"+trainOrTest));
        int n=featureMatrix.size();
        int max=-1;

        //获得矩阵列数
        for(int i=0;i<n;i++)
            max=Math.max(max,featureMatrix.getRow(i).values.length);

        Alphabet alphabet= new Alphabet(featureTypes);
        //写入矩阵数据
        for(int i=0;i<n;i++){
            MatrixRow mr=featureMatrix.getRow(i);
            FeatureVector feature_vector = new FeatureVector(alphabet, mr.featureTypes, mr.values);
            if(mr.instance.isPositive()) {
                fw.write(mr.instance.toString()+" ");
            } else {
                // fw.write(i+"\t"+n+"\t"+featureTypes.length + "\t" + 0.0 + ";");
                fw.write(mr.instance.toString()+" ");
            }
            double[] num=feature_vector.getValues();
            //System.out.println("********************featureTypes has length :"+featureTypes.length);
            //System.out.println("********************feature vector has length :"+num.length);
            int[] indice=feature_vector.getIndices();
            for(int k=0;k<indice.length;k++){
                fw.write(alphabet.lookupObject(indice[k]%alphabet.size())+"\t");
            }
            fw.write("\n");
        }
        fw.flush();
        fw.close();
    }

    public static void writeNodePair(String relation,String trainOrTest,String[] traingData) throws IOException {
        String dir=baseDir+relation;
        FileWriter fw=new FileWriter(new File(dir+"/"+trainOrTest));
        for(int i=0;i<traingData.length;i++){
            fw.write(traingData[i]+"\n");
        }
        fw.flush();
        fw.close();
    }
    public static void writeAlphabet(String relation,String[] array) throws IOException {
        String dir=baseDir+relation;
        FileWriter fw=new FileWriter(new File(dir+"/features.csv"));
        for(int i=0;i<array.length;i++)
            fw.write(array[i]+"\n");
        fw.flush();
        fw.close();
    }
    public static void writeNodePairInstance(String relation,String trainOrTest,Instance instance) throws IOException {
        String dir=baseDir+relation;
        makeDir(dir);
        FileWriter fw=new FileWriter(new File(dir+"/"+trainOrTest),true);
        fw.write(instance.toString()+"\n");
        fw.flush();
        fw.close();
    }
}


