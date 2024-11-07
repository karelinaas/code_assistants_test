-- Человек :)
SELECT
    referrals_campaign.promocode,
    referrals_affiliate.username,
    referrals_referralstat.referrals_number,
    avg(referrals_referralstat.referrals_number) OVER (PARTITION BY referrals_referralstat.campaign_id)
FROM (
    referrals_referralstat
        INNER JOIN referrals_campaign ON referrals_referralstat.campaign_id = referrals_campaign.id
        INNER JOIN referrals_affiliate on referrals_referralstat.affiliate_id = referrals_affiliate.id
);


-- ChatGPT
SELECT
    a.username,
    c.promocode,
    rs.referrals_number,
    avg_referrals.avg_referrals
FROM
    referrals_affiliate a
JOIN
    referrals_referralstat rs ON a.id = rs.affiliate_id
JOIN
    referrals_campaign c ON rs.campaign_id = c.id
JOIN
    (
        SELECT
            campaign_id,
            AVG(referrals_number) AS avg_referrals
        FROM
            referrals_referralstat
        GROUP BY
            campaign_id
    ) AS avg_referrals ON rs.campaign_id = avg_referrals.campaign_id
ORDER BY
    a.username, c.promocode;

---- с просьбой использовать оконные функции:
SELECT
    a.username,
    c.promocode,
    rs.referrals_number,
    AVG(rs.referrals_number) OVER (PARTITION BY rs.campaign_id) AS avg_referrals
FROM
    referrals_affiliate a
JOIN
    referrals_referralstat rs ON a.id = rs.affiliate_id
JOIN
    referrals_campaign c ON rs.campaign_id = c.id
ORDER BY
    a.username, c.promocode;


-- GitHub Copilot
SELECT
    a.username,
    c.promocode,
    rs.referrals_number,
    avg_stats.avg_referrals_number,
    rs.referrals_number - avg_stats.avg_referrals_number AS difference
FROM
    referrals_referralstat rs
JOIN
    referrals_affiliate a ON rs.affiliate_id = a.id
JOIN
    referrals_campaign c ON rs.campaign_id = c.id
JOIN
    (
        SELECT
            campaign_id,
            AVG(referrals_number) AS avg_referrals_number
        FROM
            referrals_referralstat
        GROUP BY
            campaign_id
    ) avg_stats ON rs.campaign_id = avg_stats.campaign_id
ORDER BY
    a.username, c.promocode;

---- с просьбой использовать оконные функции и не выводить столбец difference:
SELECT
    a.username,
    c.promocode,
    rs.referrals_number,
    AVG(rs.referrals_number) OVER (PARTITION BY rs.campaign_id) AS avg_referrals_number
FROM
    referrals_referralstat rs
JOIN
    referrals_affiliate a ON rs.affiliate_id = a.id
JOIN
    referrals_campaign c ON rs.campaign_id = c.id
ORDER BY
    a.username, c.promocode;


-- Amazon CodeWhisperer
WITH campaign_averages AS (
    SELECT
        campaign_id,
        AVG(referrals_number) AS avg_referrals
    FROM
        referrals_referralstat
    GROUP BY
        campaign_id
)
SELECT
    ra.username AS affiliate_username,
    rc.promocode AS campaign_promocode,
    rs.referrals_number AS user_referrals,
    ROUND(ca.avg_referrals, 2) AS average_referrals,
    ROUND(rs.referrals_number - ca.avg_referrals, 2) AS difference_from_average
FROM
    referrals_referralstat rs
JOIN
    referrals_affiliate ra ON rs.affiliate_id = ra.id
JOIN
    referrals_campaign rc ON rs.campaign_id = rc.id
JOIN
    campaign_averages ca ON rs.campaign_id = ca.campaign_id
ORDER BY
    rc.promocode,
    difference_from_average DESC;

---- с просьбой использовать оконные функции и не выводить столбец difference_from_average:
SELECT
    ra.username AS affiliate_username,
    rc.promocode AS campaign_promocode,
    rs.referrals_number AS user_referrals,
    ROUND(AVG(rs.referrals_number) OVER (PARTITION BY rs.campaign_id), 2) AS average_referrals
FROM
    referrals_referralstat rs
JOIN
    referrals_affiliate ra ON rs.affiliate_id = ra.id
JOIN
    referrals_campaign rc ON rs.campaign_id = rc.id
ORDER BY
    rc.promocode,
    rs.referrals_number DESC;


-- GigaCODE
SELECT
    r.promocode,
    a.username,
    rs.referrals_number,
    (SELECT AVG(rs2.referrals_number) FROM referrals_referralstat rs2 WHERE rs2.campaign_id = rs.campaign_id) as avg_referrals
FROM
    referrals_campaign r
JOIN
    referrals_referralstat rs ON r.id = rs.campaign_id
JOIN
    referrals_affiliate a ON rs.affiliate_id = a.id;

---- с просьбой использовать оконные функции:
SELECT
    r.promocode,
    a.username,
    rs.referrals_number,
    AVG(rs2.referrals_number) OVER (PARTITION BY rs.campaign_id) as avg_referrals
FROM
    referrals_campaign r
JOIN
    referrals_referralstat rs ON r.id = rs.campaign_id
JOIN
    referrals_affiliate a ON rs.affiliate_id = a.id
JOIN
    referrals_referralstat rs2 ON r.id = rs2.campaign_id;


-- SomeCompanyGPT
SELECT
    referrals_affiliate.username,
    referrals_campaign.promocode,
    COUNT(referrals_referralstat.id) AS total_referrals,
    AVG(COUNT(referrals_referralstat.id)) OVER (PARTITION BY referrals_campaign.id) AS avg_referrals
FROM
    referrals_affiliate
JOIN
    referrals_referralstat ON referrals_affiliate.id = referrals_referralstat.affiliate_id
JOIN
    referrals_campaign ON referrals_referralstat.campaign_id = referrals_campaign.id
GROUP BY
    referrals_affiliate.username, referrals_campaign.promocode
ORDER BY
    avg_referrals DESC;
