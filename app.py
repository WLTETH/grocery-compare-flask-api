#!/usr/bin/env python3
"""
Flask backend for SA Price Compare app
This is a mock implementation - replace with actual supermarket API integrations
"""

import random
from datetime import datetime, timedelta

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/search-product", methods=["POST"])
def search_product():
    data = request.get_json()
    product_name = data.get("product_name", "").lower()
    limit = data.get("result_limit", 5)

    products = []

    if data.get("pnp") == "true":
        products += get_pnp_product_codes(data, product_name, limit)
    if data.get("woolworths"):
        products += get_woolworths_product_codes(data, product_name, limit)
    if data.get("checkers") == "true":
        products += get_checkers_product_codes(data, product_name, limit)

    return jsonify(products), 200


def get_woolworths_product_codes(data, product_name, limit):
    try:
        search_url = f"https://www.woolworths.co.za/server/searchCategory?pageURL=%2Fcat&Ntt={product_name}&Dy=1"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": "f5avraaaaaaaaaaaaaaaa_session_=HNNJIFDGMDOENNHBIFOGKALDJOIPCLDAEPPKFHDJCFAKDGAEDMHHFNELDDDIBLJJCODDBHAODIBPBALHEAEAEBPNIDJEMDGAIHJNONGACGLFMLEFNKOCHCOLGBDHMMMM; __uzma=237865d5-ecd1-4e30-aa23-20a3478494c9; __uzmb=1749235917; __uzme=8311; dtCookie=v_4_srv_6_sn_EC4F56544EB08C23E1F26D116A0368DE_perc_39245_ol_1_app-3A3d6f60b8cbe0c63f_0; TS01576f1e=0156bce788fb89c08761f1db326a597a840d5895503b5303776912be9cf3153e63274a73d1f719f859ef05a302dd2f4abe2fceb8db; TS01a6902f=0156bce788fb89c08761f1db326a597a840d5895503b5303776912be9cf3153e63274a73d1f719f859ef05a302dd2f4abe2fceb8db; SearchCookie=TT1ni1749235920915yFGibV; __ssds=3; DESKTOP_VIEW=1x4; storeId=000; dtCookie=v_4_srv_6_sn_EC4F56544EB08C23E1F26D116A0368DE_perc_39245_ol_1_app-3A3d6f60b8cbe0c63f_0_app-3Aea7c4b59f27d43eb_0; __ssuzjsr3=a9be0cd8e; __uzmaj3=bba8ca5a-f01b-4b99-acf8-eab31acec8f3; __uzmbj3=1749235920; __uzmcj3=701081056734; __uzmdj3=1749235920; __uzmlj3=OvJTOl51OttD5J4Ru3EZjhSrb1vkK0zBxNierF1IVEc=; __uzmfj3=7f6000dcbfe2ba-4ab9-4d7f-af3d-7f4eeabdf7ab17492359205280-38f111f559edb85a10; uzmxj=7f90002e0fe562-fcf2-4efd-9dbb-4f2e817563301-17492359205280-333cbee0d25a03f110; dyId=-1454661715818759983; dySession=2u8fq5063fupynsn3oqrjd1whyt8xhli; __uzmc=871311929122; __uzmd=1749235924; recent_search=Y29rZQ==; pageSpecificRootCategoryId=",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.woolworths.co.za/cat?Ntt=coke&Dy=1",
            "sec-ch-ua": '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "uzlc": "true",
            "x-dtpc": "6$235920147_889h21vRAPGOBFULCHMUMIMFMHIJJREJTFTGATH-0e0",
            "x-frame-options": "SAMEORIGIN",
            "x-requested-by": "Woolworths Online",
        }

        response = requests.get(
            search_url,
            headers=headers,
        )

        data = response.json()

        products = (
            data.get("contents")[0]
            .get("mainContent")[0]
            .get("contents")[0]
            .get("records")
        )

        result = []

        i = 0

        for product in products:
            i = i + 1

            if i > limit:
                break

            result.append(
                {
                    "name": product.get("attributes").get("p_displayName"),
                    "price": product.get("startingPrice").get("p_pl10"),
                    "barcodes": [product.get("attributes").get("p_productid")],
                    "shop": "Woolworths",
                }
            )

        return result
    except Exception as e:
        print(f"Error in search_product: {str(e)}")
        return jsonify(
            {"success": False, "error": f"Failed to search product: {str(e)}"}
        ), 500


def get_checkers_product_codes(data, product_name, limit):
    try:
        search_url = "https://www.checkers.co.za/api/catalogue/get-products-filter"

        payload = {
            "storeContexts": [],
            "filterData": {
                "filter": {
                    "showAllDisplayVariants": False,
                    "showNotRangedProducts": False,
                    "productListSource": {"search": product_name},
                    "paginationOptions": {"page": None, "pageSize": 1000},
                    "filterOptions": {
                        "dealsOnly": False,
                        "brandOptions": [],
                        "departmentOptions": [],
                        "facetOptions": [],
                    },
                    "sortOptions": None,
                },
                "displayOptions": {"includeDisplayCategoryTree": True},
            },
            "forYouBonusBuyIds": [],
            "url": None,
        }

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.7",
            "baggage": "sentry-environment=production,sentry-release=XNrBqxNfAfyqnQGUcSrG6,sentry-public_key=e91247fc7bd7560a90e5ce0c4e6c04e9,sentry-trace_id=b55b10f29e4e4992b93a7f4476a141b0,sentry-sample_rate=0,sentry-transaction=%2Fsearch,sentry-sampled=false",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": "storeContexts=%5B%7B%22storeId%22%3A%225ece6935faafe599532665b2%22%2C%22serviceOptionIds%22%3A%5B%22sixty-min-delivery%22%2C%22one-day-delivery%22%5D%2C%22brandPriority%22%3A2%2C%22hasCapacity%22%3A%5B%22sixty-min-delivery%22%2C%22one-day-delivery%22%5D%2C%22distanceFromCustomer%22%3A0.005583459286111866%2C%22returnServiceOptionIds%22%3Anull%2C%22hasReturnCapacity%22%3Anull%7D%2C%7B%22storeId%22%3A%225ecf9cc7f5d049b9a1166932%22%2C%22serviceOptionIds%22%3A%5B%22sixty-min-delivery%22%5D%2C%22brandPriority%22%3A5%2C%22hasCapacity%22%3A%5B%22sixty-min-delivery%22%2C%22one-day-delivery%22%5D%2C%22distanceFromCustomer%22%3A0.01125369042655576%2C%22returnServiceOptionIds%22%3Anull%2C%22hasReturnCapacity%22%3Anull%7D%2C%7B%22storeId%22%3A%22670e8b8097db005ed4f90051%22%2C%22serviceOptionIds%22%3A%5B%22one-day-delivery%22%5D%2C%22brandPriority%22%3A4%2C%22hasCapacity%22%3A%5B%22sixty-min-delivery%22%2C%22one-day-delivery%22%5D%2C%22distanceFromCustomer%22%3A0.005583459286111866%2C%22returnServiceOptionIds%22%3Anull%2C%22hasReturnCapacity%22%3Anull%7D%5D; storeids=5ece6935faafe599532665b2-5ecf9cc7f5d049b9a1166932-670e8b8097db005ed4f90051; istio-storeIds=5ece6935faafe599532665b2-5ecf9cc7f5d049b9a1166932-670e8b8097db005ed4f90051; aws-waf-token=4a5452bb-014d-43a2-a74a-e6b13a02a6bb:CgoAjH5/qSiMAAAA:yEVLggcnmaL3VHmTmMfqBf2I6ekRf/71JDZYVTeqBGzoVToj4z3+FNxQtD3WUbz0Y6LoS1cLgHe7YhLXPI/Ttk/U8rjYVeVkocX1fLBdhpnoWEXzfh//c4/Et4aby1BoYX2DPxnQnr/crk1lYLmMz7H/MrQrw/nfE93eWidbgJOhvJTTtwM40pa557XJFCHkMrm00SlCRFwbNiyVuTxmD3ZIZ4353joXPxU5jonWCt5k1l9vW9Md4jCu6P8Ryp5kGF+P1f1SWKyQK9NhRfZr9l1fzB5DCkeH",
            "origin": "https://www.checkers.co.za",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.checkers.co.za/search?Search=coke",
            "sec-ch-ua": '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "sentry-trace": "b55b10f29e4e4992b93a7f4476a141b0-9f576027044c61f3-0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        }

        response = requests.post(
            search_url,
            json=payload,
            headers=headers,
        )

        data = response.json()

        products = data.get("products", [])

        result = []

        i = 0

        for product in products:
            i = i + 1

            if i > limit:
                break

            result.append(
                {
                    "name": product.get("name"),
                    "price": product.get("priceWithoutDecimal") / 100,
                    "barcodes": product.get("barcodes"),
                    "shop": "Checkers",
                }
            )

        return result
    except Exception as e:
        print(f"Error in search_product: {str(e)}")
        return jsonify(
            {"success": False, "error": f"Failed to search product: {str(e)}"}
        ), 500


def add_pnp_barcodes(products):
    for product in products:
        prod_code = product.get("barcodes")

        url = f"https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/{prod_code}"
        params = {
            "fields": "DEFAULT,averageRating,images(FULL),classifications,manufacturer,numberOfReviews,categories(FULL),baseOptions,baseProduct,variantOptions,variantType,productDetailsDisplayInfoResponse,quantityType",
            "storeCode": "WC21",
            "scope": "variants",
            "lang": "en",
            "curr": "ZAR",
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.pnp.co.za/search/coke",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-anonymous-consents": "%5B%5D",
            "x-dtpc": "5$152835040_670h65vCUWQAVPETMAPNRCAHESVRRQOIMPBKCMW-0e0",
            "x-pnp-cache-key": "anonymous",
            "cookie": (
                "dtCookie=v_4_srv_5_sn_862D5BF05C98523DFA56674670DAD68F_perc_100000_ol_0_mul_1_app-3A2ce7406a2949d129_0; "
                "rxVisitor=1742564822278DKN30ID5AP8SOAIUS1BAE90ONSAK4P8D; dtSa=-; "
                "ConstructorioID_session_id=1; ConstructorioID_client_id=dff7dc3f-1480-4265-8f1f-d97d6da729ba; "
                'ConstructorioID_session={"sessionId":1,"lastTime":1749154050570}; '
                "route=e940f2f0ad3ae09d004a58eb722d3d92; dtLatC=1; "
                "rxvt=1749156094247|1749152835045; "
                "dtPC=5$152835040_670h65vCUWQAVPETMAPNRCAHESVRRQOIMPBKCMW-0e0"
            ),
        }

        response = requests.get(url, headers=headers, params=params)

        data = response.json()

        barcode = (
            data.get("productDetailsDisplayInfoResponse")
            .get("productDetailDisplayInfos")[0]
            .get("displayInfoFields")
        )

        for val in barcode:
            if val.get("name") == "Barcode":
                # barcodes.append(val.get("values")[0].get("value"))
                product["barcodes"] = [val.get("values")[0].get("value")]
                break

    return products


def get_pnp_product_codes(data, product_name, limit):
    try:
        print(f"Searching for product: {product_name}")

        search_url = f"https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search?fields=products(sponsoredProduct%2ConlineSalesAdId%2ConlineSalesExtendedAdId%2Ccode%2Cname%2CbrandSellerId%2CaverageWeight%2Csummary%2Cprice(FULL)%2Cimages(DEFAULT)%2Cstock(FULL)%2CaverageRating%2CnumberOfReviews%2CvariantOptions%2CmaxOrderQuantity%2CproductDisplayBadges(DEFAULT)%2CallowedQuantities(DEFAULT)%2Cavailable%2CquantityType%2CdefaultQuantityOfUom%2CinStockIndicator%2CdefaultUnitOfMeasure%2CpotentialPromotions(FULL)%2CcategoryNames)%2Cfacets%2Cbreadcrumbs%2Cpagination(DEFAULT)%2Csorts(DEFAULT)%2CfreeTextSearch%2CcurrentQuery%2CresponseJson%2CseoCategoryContent%2CseoCategoryTitle%2CrefinedContent%2CcategoryDescription%2CkeywordRedirectUrl&query={product_name}&pageSize=72&storeCode=WC21&lang=en&curr=ZAR"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.6",
            "cache-control": "no-cache",
            "content-length": "2",
            "content-type": "application/json",
            "cookie": 'dtCookie=v_4_srv_5_sn_862D5BF05C98523DFA56674670DAD68F_perc_100000_ol_0_mul_1_app-3A2ce7406a2949d129_0; rxVisitor=1742564822278DKN30ID5AP8SOAIUS1BAE90ONSAK4P8D; dtSa=-; ConstructorioID_session_id=1; ConstructorioID_client_id=dff7dc3f-1480-4265-8f1f-d97d6da729ba; ConstructorioID_session={"sessionId":1,"lastTime":1749152835102}; dtLatC=1; route=e940f2f0ad3ae09d004a58eb722d3d92; rxvt=1749154682625|1749152835045; dtPC=5$152835040_670h50vCUWQAVPETMAPNRCAHESVRRQOIMPBKCMW-0e0',
            "origin": "https://www.pnp.co.za",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.pnp.co.za/search/coke",
            "sec-ch-ua": '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-anonymous-consents": "%5B%5D",
            "x-dtpc": "5$152835040_670h50vCUWQAVPETMAPNRCAHESVRRQOIMPBKCMW-0e0",
            "x-dtreferer": "https://www.pnp.co.za/",
            "x-pnp-cache-key": "anonymous",
            "x-pnp-search-client-id": "dff7dc3f-1480-4265-8f1f-d97d6da729ba",
            "x-pnp-search-session-id": "1",
        }

        response = requests.post(
            search_url,
            json={},
            headers=headers,
        )

        data = response.json()

        products = data.get("products", [])

        result = []

        i = 0

        for product in products:
            i = i + 1

            if i > limit:
                break

            result.append(
                {
                    "name": product.get("name"),
                    "price": product.get("price").get("value"),
                    "shop": "Pick n Pay",
                    "barcodes": product.get("code"),
                }
            )
            # print(
            #     f"{product.get('name')} -> {product.get('price').get('formattedValue')} ({product.get('code')})"
            # )

        return add_pnp_barcodes(result)
    except Exception as e:
        print(f"Error in search_product: {str(e)}")
        return jsonify(
            {"success": False, "error": f"Failed to search product: {str(e)}"}
        ), 500


@app.route("/api/cache", methods=["POST"])
def get_cache():
    """Get cached results (mock implementation)"""
    try:
        # For now, return no cache (you'll implement actual caching logic)
        return jsonify({"success": False, "message": "No cached results found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/cache/update", methods=["POST"])
def update_cache():
    """Update cache with new results (mock implementation)"""
    try:
        data = request.get_json()
        print(f"Cache update request: {data.get('query')}")

        # You'll implement actual cache storage here
        # For now, just acknowledge the request
        return jsonify({"success": True, "message": "Cache updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    print("Starting SA Price Compare Flask backend...")
    print("Available endpoints:")
    print("  POST /api/search-product - Search by product name")
    print("  POST /api/search-barcode - Search by barcode")
    print("  POST /api/cache - Get cached results")
    print("  POST /api/cache/update - Update cache")
    print("  GET /api/health - Health check")

    app.run(debug=True, host="0.0.0.0", port=5000)
