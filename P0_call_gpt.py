from inbxo import Questions as Q

domain = "cpp.edu"
result = Q["email"](domain)

if result["is_academic"] and result["country_of_origin_ISO_3166_alpha2"] == "US":
    new_result = Q["academic"](result["expanded_name"])
    result = {**result, **new_result}
print(result)
