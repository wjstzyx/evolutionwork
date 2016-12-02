

     SELECT     stock, SUM(Expr1 * 2) AS Expr1
FROM         (SELECT     dbo.p_follow.stock, ROUND(SUM(dbo.Trading_logSymbol.P * dbo.P_BASIC.P_size * dbo.AC_RATIO.ratio / 100 * dbo.p_follow.ratio / 100), 0) AS Expr1
                       FROM          dbo.Trading_logSymbol INNER JOIN
                                              dbo.P_BASIC ON dbo.P_BASIC.ST = dbo.Trading_logSymbol.ST INNER JOIN
                                              dbo.AC_RATIO ON dbo.AC_RATIO.AC = dbo.P_BASIC.AC AND dbo.AC_RATIO.Stock = dbo.P_BASIC.STOCK AND 
                                              dbo.AC_RATIO.type = dbo.P_BASIC.type INNER JOIN
                                              dbo.p_follow ON dbo.p_follow.F_ac = dbo.P_BASIC.AC AND dbo.p_follow.type = dbo.P_BASIC.type
                       WHERE      (dbo.p_follow.AC = 'StepMultiI300w') AND (LEFT(dbo.Trading_logSymbol.tradetime, 16) = LEFT(dbo.Trading_logSymbol.EnterTime, 16))
                       GROUP BY dbo.p_follow.stock) AS a
GROUP BY stock



SELECT     STOCK, Expr1   FROM  dbo.Fun_account_position('666061010') AS Fun_account_position_1