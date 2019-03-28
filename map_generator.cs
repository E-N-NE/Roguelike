using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

public static class MyArrayExtensions
{

    public static void Populate1D<T>(this T[] originalArray, T with)
    {
        for(int i = 0; i < originalArray.Length; i++)
        {
            originalArray[i] = with;
        }
    }

    public static void Populate2D<T>(this T[,] originalArray, T with)
    {
        for(int i = 0; i < originalArray.GetLength(0); i++)
        {
            for(int j = 0; j < originalArray.GetLength(1); j++)
            {
                originalArray[i, j] = with;
            }
        }
    }

}

public class Condition
{
    public int _Minimum { private get; }
    public int _Maximum { private get; }
    // Minimum and maximum value in tile for condition to be true.
    public (int X, int Y) Size { get; }
    // Area in which condition scans tiles.
    public int GetTile { get; }
    // For which tile condition scans.
    public int SetTile { get; }
    // Which tile will be placed if condition is true.
    public bool Outsider { get; }
    // Default value for tile outside map.
    public double _Probability { private get; }
    // Probability for tile to be registered.

    public Condition(int minimum, int maximum,
                     int sizeX, int sizeY,
                     int getTile, int setTile,
                     bool outsider = true, int probability = 100)
    {
        this._Minimum = minimum;
        this._Maximum = maximum;
        this._Probability = probability;
        this.Size = (X : sizeX, Y : sizeY)
        this.GetTile = getTile;
        this.SetTile = setTile;
        this.Outsider = outsider;
    }

    public bool checkCondition(int number, int percent)
    {
        return ((number >= this._Minimum) && (number <= this._Maximum)
             && (percent < this._Probability));
    }
}

public class Rule
{
    public int ConditionCount { get; }
    public Condition[] Conditions { get; }

    public Rule(Condition[] cs)
    {
        this.ConditionCount = cs.Length;
        this.Conditions = cs;
    }
}

public class RuleSet
{
    public int RuleCount { get; }
    public Rule[] Rules { get; }

    public RuleSet(Rule[] rs)
    {
        this.RuleCount = rs.Length;
        this.Rules = rs;
    }
}

public class MapHandler
{
    public (int X, int Y) _Size { private get; }
    public RuleSet _RuleSet { private get; }
    public (double[] InitialDistribution,) _AdditionalInfo { private get; }

    public var Map { get; } = new int[_Size.X, _Size.Y];
    public var _Random { private get; } = new Random();

    public MapHandler(int sizeX, int sizeY, int ruleSet)
    {
        this._Size = (X : sizeX, Y : sizeY)
        this._RuleSet = ruleSet;
        // Not introducing additional info yet.
        GenerateMap();
    }

    private void GenerateMap()
    {
        GenerateInitial();
        RunRuleSet();
    }

    private void GenerateInitial()
    {
        Parallel.For(0, _Size.X, x =>
        {
            for (int y = 0; y < _Size.Y; y++)
            {
                SetTile(x, y);
            }
        });
    }

    private void SetTile(int x, int y)
    {
        using initialDistribution = _AdditionalInfo.InitialDistribution;
        double result = _Random.NextDouble();
        for (int i = 0; i < GetLength(initialDistribution); i++)
        {
            if (result < initialDistribution[i])
            {
                this.Map[x, y] = i;
                return;
            }
            result -= initialDistribution[i];
        }
    }

    private void RunRuleSet()
    {
        foreach (Rule rule in _RuleSet.Rules)
            RunRule(rule);
    }

    private void RunRule(Rule rule)
    {
        Parallel.For(0, _Size.X, x => // May be good to make class Position,
        {                             // with size comparison and Next() method.
            for (int y = 0; y < _Size.Y; y++)
            {
                foreach (Condition condition in rule.Conditions)
                {
                    int numberOfRightTiles = Scan(x, y, condition);
                    if ();
                }
            }
        });
    }

    private int Scan(int x0, int y0, Condition condition) // This better be
    {                                                     // optimal.
        int minX = max(x0 - condition.Size.X, 0);
        int maxX = min(x0 + condition.Size.X, _Size.X);
        int minY = max(y0 - condition.Size.Y, 0);
        int maxY = min(y0 + condition.Size.Y, _Size.Y);
        int areaOutsideBorders = (condition.Size.X*2 + 1)
                               * (condition.Size.Y*2 + 1)
                               - (maxX - minX) * (maxY - minY)
        for (int x = ; x <= ; x++)
        {
            for (int y = y0 - condition.Size.Y; y <= y0 + condition.Size.Y; y++)
            {
                if ()
            }
        }
    }
}
