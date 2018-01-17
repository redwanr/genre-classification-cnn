select 
       p.product_id, 
       game_name, 
       'https://store.playstation.com/en-us/product/' || PMT_PRODUCT_ID as product_url,
       pe.psncat_genre, 
       p.game_genre, 
       case when game_genre in ('Not available', 'Miscellaneous')  then 
                     case when pe.psncat_genre = 'Sport Games' then 'Sports'
                          when pe.psncat_genre = 'Role-Playing' then 'RPG'
                           when pe.psncat_genre = 'Racing' then 'Driving/Racing'
                           when pe.psncat_genre = 'Action' then 'Action/Adventure'
                           else pe.psncat_genre
                     end
              else game_genre
              end as final_genre
from dim_product p
       join DIM_PRODUCT_EXT pe
              on p.product_id = pe.product_id 
where psncat_product_class = 'Full Game'
and pmt_playable_platform_full_desc = 'PS4'
and pmt_primary_classification <> 'Disc Based Game'

