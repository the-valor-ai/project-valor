# Changelog

## Version 2.0.0 - Complete System Refactor

### Major Changes

#### Removed Files
- app/main.py (old mango-specific version)
- app/model_loader.py (old TensorFlow implementation)
- app/predictor.py (old inference logic)
- app/utils.py (unused utility functions)
- train.py (old training script)
- TRAINING.md
- OFFLINE_STRATEGY.md
- FIXES_APPLIED.md
- START_HERE.md
- README_V2.md
- QUICKSTART.md
- test_setup.py
- test_api.py
- start_server.bat
- models/fruit_classifier.keras (old model files)
- models/fruit_classifier1.h5 (old model files)
- models/fruit_model.h5 (old model files)
- models/class_labels.json (old labels)
- fruit-classification-using-cnn-98.ipynb (reference notebooks)
- fruits-and-vegetables-image-mobilenetv2 (1).ipynb (reference notebooks)
- .github/ (issue templates directory)

#### Updated Files

**app/ai_service.py**
- Changed from mango-specific to general produce analysis
- Updated prompts to support all fruits and vegetables
- Removed mango-only disease focus
- Generalized classification from "is_mango" to "fruit_type"
- Updated ripeness assessment for all produce types
- Removed emojis and unnecessary formatting characters

**app/config.py**
- Updated translations to be produce-generic
- Changed "mango_detected" to "produce_detected"
- Changed "not_mango" to "not_produce"
- Removed emojis from translation strings
- Fixed language translation inconsistencies

**app/main.py**
- Complete rewrite for general produce analysis
- Removed all emojis from API descriptions
- Removed mango-specific documentation
- Simplified endpoint descriptions
- Cleaned up response examples
- Removed persona-specific documentation (Ade, Ifeoma, Tunde)
- Updated API title and descriptions

**README.md**
- New clean documentation without emojis
- Generic produce analysis focus
- Removed mango-specific content
- Simplified structure
- Professional tone throughout

### API Changes

#### Classification Endpoint
**Before:**
- Returned `is_mango: true/false`

**After:**
- Returns `fruit_type: "mango"` (or any fruit/vegetable)

#### Ripeness Endpoint
**Before:**
- Focused on mango-specific characteristics
- African market specific language

**After:**
- Generic produce ripeness assessment
- Applicable to all fruits and vegetables

#### Disease Endpoint
**Before:**
- TOP 5 Nigerian mango diseases
- Mango-specific conditions

**After:**
- Common fruit and vegetable diseases
- General produce defects and damage

### Language Support

Maintained support for:
- English (en)
- Yoruba (yo)
- Igbo (ig)
- Hausa (ha)

Updated translations to be produce-generic instead of mango-specific.

### Technical Improvements

- Improved JSON parsing with regex fallback
- Better error handling
- Cleaner code structure
- Removed formatting characters (em dashes, asterisks, emojis)
- Professional API documentation

### Breaking Changes

1. **Classification Response Format**
   - Old: `{"is_mango": true, "variety": "Kent"}`
   - New: `{"fruit_type": "mango", "variety": "Kent"}`

2. **Full Analysis Flow**
   - Old: Only proceeded if produce was a mango
   - New: Analyzes any fruit or vegetable

3. **Translation Keys**
   - Old: `mango_detected`, `not_mango`
   - New: `produce_detected`, `not_produce`

### Migration Guide

If migrating from v1.x:

1. Update client code to use `fruit_type` instead of `is_mango`
2. Remove mango-specific logic from integrations
3. Update environment variables if needed
4. Test with various produce types (not just mangoes)

### Known Issues

- Offline mode not yet implemented
- No model files included (online API only)
- Rate limiting not implemented

### Future Plans (v2.1)

- Implement offline TensorFlow Lite models
- Add batch processing endpoint
- User authentication system
- Analysis history tracking
- Performance optimizations

## Version 1.0.0 - Initial Release

- Mango-specific analysis
- Basic classification and ripeness detection
- Limited disease detection
- Multi-language support
