using System;
using System.Collections.Generic;

public class Condition
{
  public int Minimum { get; set; }
  public int Maximum { get; set; }
  public int SizeX { get; set; }
  public int SizeY { get; set; }
  public int GetTile  { get; set; }
  public int SetTile  { get; set; }
  public bool Default  { get; set; }

  public Condition(int mn, int mx, int sx, int sy, int gttr, int sttr, bool df)
  {
    this.Minimum = mn;
    this.Maximum = mx;
    this.SizeX = sx;
    this.SizeY = sy;
    this.GetTile = gttr;
    this.SetTile = sttr;
    this.Default = df;
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

	public int MapWidth		{ get; set; }
	public int MapHeight		{ get; set; }
	public int PercentAreWalls	{ get; set; }
  public RuleSet MapRuleSet  { get; set; }

	public MapHandler(int mw, int mh, int paw, RuleSet rs)
	{
		this.MapWidth = mw;
		this.MapHeight = mh;
		this.PercentAreWalls = paw;
    this.MapRuleSet = rs;
		RandomFillMap();
    MakeAllCaverns();
    PrintMap();
	}

  public void MakeAllCaverns()
  {
    int[,] NewMap = new int[MapWidth,MapHeight];
    for(int RulePointer=0; RulePointer < MapRuleSet.RuleCount; RulePointer++)
    {
      for(int column=0, row=0; row <= MapHeight-1; row++)
      {
        for(column = 0; column <= MapWidth-1; column++)
        {
          NewMap[column,row] = PlaceThingLogic(column,row,RulePointer);
        }
      }
      Map = NewMap;
    }
  }

	public int PlaceThingLogic(int x,int y, int RulePointer)
	{
		for(int conditionPointer=0;
        conditionPointer < MapRuleSet.Rules[RulePointer].ConditionCount; conditionPointer++)
    {
      var thingsAround = GetAdjacentThings(x,y,
                        MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].SizeX,MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].SizeY,
                        MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].GetTile,
                        MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].Default);
      if(MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].Minimum <= thingsAround &&
         MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].Maximum >= thingsAround)
      {
        if(MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].SetTile == -1)
          return Map[x,y];
        else
          return MapRuleSet.Rules[RulePointer].Conditions[conditionPointer].SetTile;
      }
    }
    return Map[x,y];
	}

	public int GetAdjacentThings(int x,int y,int scopeX,int scopeY,
                               int thing, bool Default)
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
				if(IsThing(iX,iY,thing,Default))
					thingCounter += 1;
		return thingCounter;
	}

	bool IsThing(int x,int y, int thing, bool Default)
	{
		// Consider out-of-bound a wall
		if( IsOutOfBounds(x,y) )
		{
			return Default;
		}

		if( Map[x,y]==thing	 )
		{
			return true;
		}

		return false;
	}

	bool IsOutOfBounds(int x, int y)
	{
		if( x<0 || y<0 )
		{
			return true;
		}
		else if( x>MapWidth-1 || y>MapHeight-1 )
		{
			return true;
		}
		return false;
	}

	public void PrintMap()
	{
		Console.Clear();
		Console.Write(MapToString());
	}

	string MapToString()
	{
		string returnString = string.Join(" ", // Seperator between each element
		                                  "Width:",
		                                  MapWidth.ToString(),
		                                  "\tHeight:",
		                                  MapHeight.ToString(),
		                                  "\t% Walls:",
		                                  PercentAreWalls.ToString(),
		                                  Environment.NewLine
		                                 );


		List<string> mapSymbols = new List<string>();
		mapSymbols.Add(".");
		mapSymbols.Add("#");
		mapSymbols.Add("~");

		for(int column=0,row=0; row < MapHeight; row++ ) {
			for( column = 0; column < MapWidth; column++ )
			{
				returnString += mapSymbols[Map[column,row]];
			}
			returnString += Environment.NewLine;
		}
		return returnString;
	}

	public void BlankMap()
	{
		for(int column=0,row=0; row < MapHeight; row++) {
			for(column = 0; column < MapWidth; column++) {
				Map[column,row] = 0;
			}
		}
	}

	public void RandomFillMap()
	{
		// New, empty map
		Map = new int[MapWidth,MapHeight];

		int mapMiddle = 0; // Temp variable
		for(int column=0,row=0; row < MapHeight; row++) {
			for(column = 0; column < MapWidth; column++)
			{
				// If coordinants lie on the the edge of the map (creates a border)
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
				// Else, fill with a wall a random percent of the time
				else
				{
					mapMiddle = (MapHeight / 2);

					if(row == mapMiddle)
					{
						Map[column,row] = 0;
					}
					else
					{
						Map[column,row] = RandomPercent(PercentAreWalls);
					}
				}
			}
		}
	}

	int RandomPercent(int percent)
	{
		if(percent>=rand.Next(1,101))
		{
			return 1;
		}
		return 0;
	}



  public static void Main()
  {
    Condition CONDITION_5      = new Condition(5,9,1,1,1,1,true);
    Condition CONDITION_LONELY = new Condition(0,2,2,2,1,1,true);
    Condition CONDITION_ELSE_0 = new Condition(0,1,0,0,0,0,false);
    Rule RULE_5                 = new Rule(new Condition[]{CONDITION_5,CONDITION_ELSE_0});
    Rule RULE_COMPLEXITY        = new Rule(new Condition[]{CONDITION_5,CONDITION_LONELY,CONDITION_ELSE_0});
    Rule RULE_LONELY            = new Rule(new Condition[]{CONDITION_LONELY});
    RuleSet RULESET_STANDARD     = new RuleSet(new Rule[]{RULE_5,RULE_5,RULE_5,RULE_5,RULE_5,RULE_LONELY});
    MapHandler myMap              = new MapHandler(40,40,50,RULESET_STANDARD);
  }
}
