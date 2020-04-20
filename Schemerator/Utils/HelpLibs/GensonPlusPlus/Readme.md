What change in GensonPlusPlus

we take the project Genson (from Github) and change him.

- change "required" field to be an optional. (object.py was change for this)
- add support in minLength and maxLength in numbers and strings.
 (generators/scalar.py and generators/MinMax.py was change for this)
- add "additionalProperties = False" in objects. (object.py and also node.py was changed for this)
- add "additionalItems = False" in arrays. (array.py was changed for this)
-