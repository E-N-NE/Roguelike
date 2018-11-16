using System;
using System.Collections.Generic;
using System.Linq;

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
    for(int j, i = 0; i < originalArray.GetLength(0); i++)
    {
      for(j = 0; j < originalArray.GetLength(1); j++)
      {
        originalArray[i, j] = with;
      }
    }
  }

}

public class Condition
{
  public int Minimum { get; set; }
  public int Maximum { get; set; }
  public int SizeX { get; set; }
  public int SizeY { get; set; }
  public int GetTile  { get; set; }
  public int SetTile  { get; set; }
  public bool Outsider  { get; set; }
  public int Probability  { get; set; }

  public Condition(int mn, int mx, int sx, int sy, int gt, int st,
                   bool outsider = true, int probability = 100)
  {
    this.Minimum = mn;
    this.Maximum = mx;
    this.SizeX = sx;
    this.SizeY = sy;
    this.GetTile = gt;
    this.SetTile = st;
    this.Outsider = outsider;
    this.Probability = probability;
  }

  public bool checkCondition(int number, int percent)
  {
    return ((this.Minimum <= number)
         && (this.Maximum >= number)
         && (this.Probability > percent));
  }
}

public class Rule
{
  public int ConditionCount  { get; set; }
  public Condition[] Conditions  { get; set; }

  public Rule(Condition[] cs)
  {
    this.ConditionCount = cs.Length;
    this.Conditions = cs;
  }
}

public class RuleSet
{
  public int RuleCount  { get; set; }
  public Rule[] Rules  { get; set; }

  public RuleSet(Rule[] rs)
  {
    this.RuleCount = rs.Length;
    this.Rules = rs;
  }
}

public class MapHandler
{
  System.Random rand = new System.Random();

  public int[,] Map;

  public int MapWidth    { get; set; }
  public int MapHeight    { get; set; }
  public int PercentAreWalls  { get; set; }
  public int MinimalPlayZone  { get; set; }
  public RuleSet MapRuleSet  { get; set; }
  public List<int> MapClocky  { get; set; }
  public bool[,] PlayZone  { get; set; }

  public MapHandler(int mw, int mh, int paw, int mpz, RuleSet rs)
  {
    this.MapWidth = mw;
    this.MapHeight = mh;
    this.PercentAreWalls = paw;
    this.MinimalPlayZone = mpz;
    this.MapRuleSet = rs;
    this.MapClocky = Clocky(1, 0);
    do
    {
      PlayZone = new bool[MapWidth, MapHeight];
      PlayZone.Populate2D(false);
      RandomMap();
      MakeAllCaverns();
      Border();
      FillOutFromRandom();
    } while(CalculatePlayZone() < this.MinimalPlayZone);
    PrintMap();
  }

  int CalculatePlayZone()
  {
    int returnee = 0;
    for(int column, row = 0; row <= MapHeight-1; row++)
    {
      for(column = 0; column <= MapWidth-1; column++)
      {
        if(this.PlayZone[column,row])
          returnee++;
      }
    }
    return returnee;
  }

  List<int> Clocky(int range, int disrange)
  {
    List<int> clocky = new List<int>(9*range*range);
    for(int j, i = -range; i <= range; i++)
    {
      for(j = -range; j <= range; j++)
      {
        if(i > disrange || i < -disrange || j > disrange || j < -disrange)
        {
          clocky.Add(i + j*MapWidth);
        }
      }
    }
    return clocky;
  }

  void MakeAllCaverns()
  {
    for(int RulePointer = 0; RulePointer < MapRuleSet.RuleCount;
        RulePointer++)
    {
      int[,] NewMap = new int[MapWidth,MapHeight];
      for(int column, row = 0; row <= MapHeight-1; row++)
      {
        for(column = 0; column <= MapWidth-1; column++)
        {
          NewMap[column,row] = PlaceThingLogic(column, row, RulePointer);
        }
      }
      Map = NewMap;
    }
  }

  int PlaceThingLogic(int x, int y, int RulePointer)
  {
    for(int conditionPointer=0;
        conditionPointer < MapRuleSet.Rules[RulePointer].ConditionCount;
        conditionPointer++)
    {
      Condition currentCondition = MapRuleSet.Rules[RulePointer].
                                   Conditions[conditionPointer];
      var thingsAround = GetAdjacentThings(x, y,
                         currentCondition.SizeX,currentCondition.SizeY,
                         currentCondition.GetTile,
                         currentCondition.Outsider);
      if(currentCondition.checkCondition(thingsAround, RandomPercent()))
      {
        if(currentCondition.SetTile == -1)
          return Map[x,y];
        else
          return currentCondition.SetTile;
      }
    }
    return Map[x,y];
  }

  int GetAdjacentThings(int x,int y,int scopeX,int scopeY,
                               int thing, bool outsider)
  {
    int startX = x - scopeX;
    int startY = y - scopeY;
    int endX = x + scopeX;
    int endY = y + scopeY;

    int iX = startX;
    int iY = startY;

    int thingCounter = 0;

    for(iY = startY; iY <= endY; iY++)
      for(iX = startX; iX <= endX; iX++)
        if(IsThing(iX, iY, thing, outsider))
          thingCounter += 1;
    return thingCounter;
  }

  bool IsThing(int x,int y, int thing, bool outsider)
  {
    // Consider out-of-bound a wall
    if(IsOutOfBounds(x, y))
    {
      return outsider;
    }

    if(Map[x,y] == thing)
    {
      return true;
    }

    return false;
  }

  bool IsOutOfBounds(int x, int y)
  {
    if( x < 0 || y < 0 )
    {
      return true;
    }
    else if( x > MapWidth-1 || y > MapHeight-1 )
    {
      return true;
    }
    return false;
  }

  void PrintMap()
  {
    Console.Clear();
    Console.Write(MapToString());
  }

  string MapToString()
  {
    string returnString = "";

    char[] mapSymbols = new char[4]{'.','#','~','8'};

    for(int column = 0, row = 0; row < MapHeight; row++ )
    {
      for(column = 0; column < MapWidth; column++ )
      {
        returnString += mapSymbols[Map[column,row]];
      }
      returnString += Environment.NewLine;
    }
    return returnString;
  }

  void FillOutFromRandom()
  {
    int x;
    int y;
    do
    {
      x = rand.Next(0, MapWidth);
      y = rand.Next(0, MapHeight);
    } while (Map[x,y] != 0);
    FillOutFrom(x, y);
  }

  void FillOutFrom(int x, int y)
  {
    PlayZone[x, y] = true;
    List<int> front = new List<int>(MapWidth*MapHeight);
    front.Add(x + y*MapWidth);
    while(front.Count > 0)
    {
      front = NewFront(front);
    }
    for(int j, i = 0; i < MapWidth; i++)
    {
      for(j = 0; j < MapHeight; j++)
      {
        if(!PlayZone[i,j] && Map[i,j] == 0)
          Map[i,j] = 1;
      }
    }
  }

  List<int> NewFront(List<int> oldFront)
  {
    List<int> newFront = new List<int>(MapWidth*MapHeight);
    int x, y;
    foreach(int fronter in oldFront)
    {
      foreach(int clocker in MapClocky)
      {
        x = (fronter+clocker) % MapWidth;
        y = (fronter+clocker) / MapWidth;
        if(Map[x,y] == 0 && !PlayZone[x,y])
        {
          PlayZone[x,y] = true;
          newFront.Add(fronter+clocker);
        }
      }
    }
    return newFront;
  }

  void BlankMap()
  {
    for(int column, row = 0; row < MapHeight; row++)
    {
      for(column = 0; column < MapWidth; column++)
      {
        Map[column,row] = 0;
      }
    }
  }

  void Border()
  {
    for(int column = 0,row = 0; row < MapHeight; row++)
    {
      for(column = 0; column < MapWidth; column++)
      {
        if(column == 0)
        {
          Map[column,row] = 3;
        }
        else if (row == 0)
        {
          Map[column,row] = 3;
        }
        else if (column == MapWidth-1)
        {
          Map[column,row] = 3;
        }
        else if (row == MapHeight-1)
        {
          Map[column,row] = 3;
        }
      }
    }
  }

  void RandomMap()
  {
    Map = new int[MapWidth,MapHeight];
    for(int column = 0,row = 0; row < MapHeight; row++)
    {
      for(column = 0; column < MapWidth; column++)
      {
        // Creates a border
        if(column == 0)
        {
          Map[column,row] = 1;
        }
        else if (row == 0)
        {
          Map[column,row] = 1;
        }
        else if (column == MapWidth-1)
        {
          Map[column,row] = 1;
        }
        else if (row == MapHeight-1)
        {
          Map[column,row] = 1;
        }
        else
        {
          Map[column,row] = (PercentAreWalls > RandomPercent()) ? 1 : 0;
        }
      }
    }
  }

  int RandomPercent()
  {
    return rand.Next(0,100);
  }



  public static void Main(string[] args)
  {
    Condition CONDITION_5          = new Condition(5,9,1,1,1,1);
    Condition CONDITION_LONELY     = new Condition(0,3,3,3,1,1);
    Condition CONDITION_ABSOLUTE_0 = new Condition(0,1,0,0,0,0);
    Condition CONDITION_VER        = new Condition(3,5,0,2,1,1);
    Condition CONDITION_HOR        = new Condition(3,5,2,0,1,1);
    Condition CONDITION_RAND_WATER = new Condition(3,8,1,1,1,2,true,1);
    Condition CONDITION_SPRINKLE   = new Condition(0,2,1,1,1,-1);
    Condition CONDITION_FRESH_AIR  = new Condition(0,0,2,2,0,-1,false);
    Condition CONDITION_LAKE       = new Condition(1,9,1,1,2,2,false,50);
    Rule RULE_5                  = new Rule(new Condition[]{
  CONDITION_5, CONDITION_ABSOLUTE_0});
    Rule RULE_VER                = new Rule(new Condition[]{
  CONDITION_VER, CONDITION_ABSOLUTE_0});
    Rule RULE_HOR                = new Rule(new Condition[]{
  CONDITION_HOR, CONDITION_ABSOLUTE_0});
    Rule RULE_COMPLEXITY         = new Rule(new Condition[]{
  CONDITION_5, CONDITION_LONELY, CONDITION_ABSOLUTE_0});
    Rule RULE_FLOOD              = new Rule(new Condition[]{
  CONDITION_RAND_WATER});
    Rule RULE_COMPLETENESS       = new Rule(new Condition[]{
  CONDITION_SPRINKLE, CONDITION_FRESH_AIR, CONDITION_LAKE});
    RuleSet RULESET_STANDARD   = new RuleSet(new Rule[]{
 RULE_5, RULE_5, RULE_5, RULE_COMPLEXITY, RULE_5, RULE_FLOOD,
 RULE_COMPLETENESS, RULE_COMPLETENESS, RULE_COMPLETENESS});
    RuleSet RULESET_ROUGH      = new RuleSet(new Rule[]{
 RULE_5, RULE_COMPLEXITY, RULE_5, RULE_FLOOD,
 RULE_COMPLETENESS, RULE_COMPLETENESS});
    RuleSet RULESET_VER        = new RuleSet(new Rule[]{
 RULE_VER, RULE_VER, RULE_COMPLEXITY, RULE_VER});
    RuleSet RULESET_HOR        = new RuleSet(new Rule[]{
 RULE_HOR, RULE_HOR, RULE_COMPLEXITY, RULE_HOR});

    if (args.Length != 5)
      throw new ArgumentException("Invalid number of parameters, must be 5.",
       "original");

    int SIZE_X;
    int SIZE_Y;
    int WALL_PERCENT;
    int MINIMAL_PLAY_ZONE;
    RuleSet RULESET;
    Int32.TryParse(args[0], out SIZE_X);
    Int32.TryParse(args[1], out SIZE_Y);
    Int32.TryParse(args[2], out WALL_PERCENT);
    Int32.TryParse(args[3], out MINIMAL_PLAY_ZONE);
    if (args[4] == "s")
      RULESET = RULESET_STANDARD;
    else if (args[4] == "r")
      RULESET = RULESET_ROUGH;
    else if (args[4] == "v")
      RULESET = RULESET_VER;
    else if (args[4] == "h")
      RULESET = RULESET_HOR;
    else
      throw new ArgumentException("Invalid ruleset parameter.", "original");
    MapHandler myMap = new MapHandler(SIZE_X, SIZE_Y,
                                      WALL_PERCENT, MINIMAL_PLAY_ZONE,
                                      RULESET);
  }
}
