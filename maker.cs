public class Condition
{
  public int Maximum { get; set; }
  public int Minimum { get; set; }
  public int SizeX { get; set; }
  public int SizeY { get; set; }
  public int GetTile  { get; set; }
  public int SetTile  { get; set; }
  public int Default  { get; set; }

  public Condition(int mx, int mn, int sx, int sy, int gttr, int sttr, int df)
  {
    this.Maximum = mx;
    this.Minimum = mn;
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

  public Rule(int cc, Condition[] cs)
  {
    this.ConditionCount = cc;
    this.Conditions = cs;
  }
}

public class RuleSet
{
  public int RuleCount  { get; set; }
  public Rule[] Rules  { get; set; }

  public RuleSet(int rc, Rule[] rs)
  {
    this.RuleCount = rc;
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
  public int RulePointer  { get; set; }

	public MapHandler(int mw, int mh, int paw, RuleSet rs)
	{
		this.MapWidth = mw;
		this.MapHeight = mh;
		this.PercentAreWalls = paw;
    this.MapRuleSet = rs;
    this.RulePointer = 0;
		RandomFillMap();
    MakeAllCaverns();
    PrintMap();
	}

  public void MakeAllCaverns()
  {
    for(RulePointer=0; RulePointer < MapRuleSet.RuleCount; RulePointer++)
      MakeCaverns();
  }

	public void MakeCaverns()
	{
		// By initilizing column in the outter loop, its only created ONCE
		for(int column=0, row=0; row <= MapHeight-1; row++)
		{
			for(column = 0; column <= MapWidth-1; column++)
			{
				Map[column,row] = PlaceThingLogic(column,row);
			}
		}
	}

	public int PlaceThingLogic(int x,int y)
	{
		for(int condition=0;
        condition < MapRuleSet.Rules[RulePointer].ConditionCount; condition++)
    {
      if(MapRuleSet.Rules[RulePointer].Conditions[condition].Minimum <=
         GetAdjacentThings(x,y,
                           MapRuleSet.Rules[RulePointer].Conditions[condition].SizeX,MapRuleSet.Rules[RulePointer].Conditions[condition].SizeY,
                           MapRuleSet.Rules[RulePointer].Conditions[condition].GetTile,
                           MapRuleSet.Rules[RulePointer].Conditions[condition].Default)
         <= MapRuleSet.Rules[RulePointer].Conditions[condition].Maximum)
      {
        if(MapRuleSet.Rules[RulePointer].Conditions[condition].SetTile == -1)
          return Map[x,y];
        else
          return MapRuleSet.Rules[RulePointer].Conditions[condition].SetTile;
      }
      else
        continue;
    }
    return Map[x,y];
	}

	public int GetAdjacentThings(int x,int y,int scopeX,int scopeY,
                               int thing, int Default)
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

	bool IsThing(int x,int y, int thing, int Default)
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

  public void Main()
  {
    Condition CONDITION_5 = Condition(5,5,1,1,1,1,1);
    Condition CONDITION_LONELY = Condition(0,2,2,2,1,1,1);
    Rule RULE_5 = Rule(1,new Condition{CONDITION_5});
    Rule RULE_COMPLEXITY = Rule(2,new {CONDITION_5,CONDITION_LONELY});
    Ruleset RULESET_STANDARD = RuleSet(5,new {RULE_5,RULE_5,RULE_5,RULE_5,RULE_COMPLEXITY});
    MapHandler myMap = MapHandler(40,40,40,RULESET_STANDARD);
  }
}
