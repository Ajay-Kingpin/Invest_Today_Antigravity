from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

class InvestTodayState(TypedDict):
    """
    Represents the state of the investment analysis workflow.
    """
    symbol: str
    query: str
    # Use Annotated with operator.add to allow multiple nodes to contribute to reports
    reports: Annotated[Dict[str, str], operator.ior]
    final_recommendation: Optional[str]
    confidence_score: Optional[int]
    errors: List[str]
    metadata: Dict[str, Any]
