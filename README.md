# backt
# CEO WIlliam observation

1. def max_date ... perhaps it's more convenient to get a self.end_date and not to run each time function while downloading yahoo (row 33)
2. Rows 71 & 72 are the same perhaps u wanna fill 0 only if the 1st row is nan, right?
3. Row 64 well done! Master of the mergering! 
4. Rows 62 & 33 are the same no need to double use them I think.
5. From row 45 we are loosing the conection b/w 'open price' and 'close price' since in Row 66 we take Adj close. I've also seen that u dropped first line in daily returns (Row 81) which is not good. What generally I want to say is that as the first line we need to add diff b/w close/open of the 1st trading day.
6. Rows 80 & 82 are useless we talked about it already yesterday, for now I leave them but I ll remove it in the future when we discuss about what I wrote.
7. I think that creating 3 functions such as pricing, consolidated & consolidated_detailed doesn't really make a sense. I would rather make one big function. And would also help partially to solve the problem mentioned in the point 5.
8. Disregard def equal weighting  for now 

Overall great job, proud of your triple variables in "for" zip. What do you smoke?