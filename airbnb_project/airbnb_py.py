import pandas as pd

def count_of_reviews(listing_id):
    rev_group = rev_df_filtered.groupby('listing_id')
    return len(rev_group.get_group(listing_id))

def available_listings():
    avail = cal_df.groupby('available')
    return avail.get_group('t')

available_list = available_listings()

for id in rev_df_filtered['listing_id'].unique():

    list_df_filtered.loc[list_df_filtered['id'] == id, 'num_reviews'] = count_of_reviews(id)

    id_availability = available_list[available_list['listing_id'] == id]

    avail_date = id_availability['date'].to_string(index=False)
    avail_date = avail_date.replace("\n", "; ")
    list_df_filtered.loc[list_df_filtered['id'] == id, 'dates_available'] = avail_date

list_df_filtered.dropna(subset=['review_scores_rating', 'num_reviews', 'price'], inplace=True)
final_df = list_df_filtered[list_df_filtered['room_type'] != "Private room"]

breakpoint()
