import steammarket as sm

item = sm.get_tf2_item('Strange Professional Killstreak Scattergun')
for listing in item.listings:
    print(listing.price)