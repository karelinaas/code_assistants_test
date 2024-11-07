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
